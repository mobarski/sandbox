from __future__ import print_function
import numpy as np

from heapq import nlargest
from time import time
import marshal

# TODO - FEATURES:
## TODO: sparse permanence like in the temporal_pooler
## TODO: boosting: firing uses b_dec boosting_factor, which restores by b_inc per cycle
## TODO: TEST dynamic threshold (raise if score>j, lower if score<k)
## TODO: better boost_factor formula (one way? always>=1 or always<=1)
## TODO: better p_inc p_dec formula ???

# TODO - OPTIMIZATION:
## TODO: numba
## TODO: numba+cuda
## TODO: multiprocessing .learn
## TODO: multiprocessing .score
## TODO: multiprocessing .init

# REFERENCES:
## https://numenta.org/resources/HTM_CorticalLearningAlgorithms.pdf

def random_sdr(n,k):
	k = k if type(k)==int else int(k*n)
	out = set(np.random.randint(0,n,k))
	while len(out)<k:
		missing_cnt = k-len(out)
		out.update(np.random.randint(0, n, missing_cnt))
	return out

class spatial_pooler:

	def __init__(self, n, k, m=None, u=0, s_min=0,
					t=100, p_lo=70, p_hi=130,
					boost=True, b_min=0.75, b_max=1.25,
					p_inc=10, p_dec=6 ):
		"""
		Parameters
		----------
			n -- number of neurons (:int)
			k -- number of neurons to fire (:int) or proportion of neurons to fire (:float)
			m -- number of input neurons (equal to n by default) (:int or None)
			u -- number of unconnectable synapses per neuron (:int) or proportion of unconnectable synapses (:float)
			t -- connection threshold (:int)
			p_lo -- lowest permanence when initializing (:int)
			p_hi -- highest permanence when initializing (:int)
			boost -- enable overlap score boosting (:bool)
			b_min -- minimum boost factor (:int)
			b_max -- maximum boost factor (:int)
			p_inc -- permanence increase value (:int)
			p_dec -- permanence decrease value (:int)
			s_min -- minimum score (:int)
		"""
		m = m or n
		self.cfg = {}
		self.cfg['n'] = n
		self.cfg['m'] = m
		self.cfg['k'] = int(k*n) if type(k)==float else k
		self.cfg['t'] = t
		self.cfg['u'] = int(u*m) if type(u)==float else u
		self.cfg['p_inc'] = p_inc
		self.cfg['p_dec'] = p_dec
		self.cfg['p_lo'] = p_lo
		self.cfg['p_hi'] = p_hi
		self.cfg['b_min'] = b_min
		self.cfg['b_max'] = b_max
		self.cfg['boost'] = boost
		self.cfg['s_min'] = s_min
		self.activity = np.zeros(n,dtype=np.uint32)
		self.cycles = 0
		self.perm = None # synaptic permanence
		self.conn = None # synaptic connections
		self.init_synapses()

	def init_synapses(self):
		"initialize synaptic permanence and connections"
		t = self.cfg['t']
		n = self.cfg['n']
		m = self.cfg['m']
		k = self.cfg['k']
		u = self.cfg['u']
		p_lo = self.cfg['p_lo']
		p_hi = self.cfg['p_hi']
		
		conn = {x:random_sdr(m,k) for x in range(n)} # TODO: optimize
		self.conn = conn
		
		perm = np.random.randint(p_lo, t-1, (n,m), np.uint8)
		for i in range(n):
			perm[i][list(conn[i])] = np.random.randint(t, p_hi, k)
		self.perm = perm
		
		if u:
			for i in range(n):
				lowest = perm[i].argsort()[:u]
				perm[i][lowest] = 0

	@staticmethod
	def load(f):
		"load pooler from file"
		self = spatial_pooler(0,0)
		self.cfg = marshal.load(f)
		self.conn = marshal.load(f)
		self.cycles = marshal.load(f)
		n = self.cfg['n']
		self.perm = np.fromfile(f,np.uint8,n*n).reshape((n,n))
		self.activity = np.fromfile(f,np.uint32,n)
		return self

	def save(self,f,version=2):
		"save pooler to file"
		marshal.dump(self.cfg, f, version)
		marshal.dump(self.conn, f, version)
		marshal.dump(self.cycles, f, version)
		self.perm.tofile(f)
		self.activity.tofile(f)
		
	# ---[ CORE ]---------------------------------------------------------------
	
	def score(self,input):
		"calculate overlap score for every neuron"
		s_min = self.cfg['s_min']
		conn = self.conn
		score = {x:len(input & conn[x]) for x in conn}
		if s_min:
			score = {x:0 if score[x]<s_min else score[x] for x in score}
		return score

	def learn(self,input,update_conn=True,verbose=False,show_times=False):
		"learn single input"
		
		k = self.cfg['k']
		n = self.cfg['n']
		m = self.cfg['m']
		t = self.cfg['t']
		p_inc = self.cfg['p_inc']
		p_dec = self.cfg['p_dec']
		b_min = self.cfg['b_min']
		b_max = self.cfg['b_max']
		boost = self.cfg['boost']
		conn = self.conn
		perm = self.perm
		activity = self.activity
		meta = {}
		
		tx=[] # time[x]
		tx.append(time())
		
		if verbose:
			print()
			print('input',list(input))
		
		# score
		score = self.score(input)
		if verbose: print('by_score',sorted(score.items(),key=lambda x:x[1],reverse=True))
		tx.append(time())
		
		# boost
		if boost:
			target_pct = 1.0 * k / n # uniform distribution
			cycles = self.cycles or 1
			for i in score:
				activity_pct = 1.0 * activity[i] / cycles
				boost_factor = b_max if activity_pct < target_pct else b_min+(1.0-b_min)*target_pct/activity_pct # TODO: better formula
				score[i] *= boost_factor
		tx.append(time())
		
		# activate
		by_score = sorted(score.items(),key=lambda x:x[1],reverse=True)
		active = [x[0] for x in by_score[:k]] # activate k best neurons
		if verbose: print('activity',activity)
		if verbose: print('by_score',by_score)
		if verbose: print('active',active)
		tx.append(time())
		
		# record activity
		activity[active] += 1
		self.cycles += 1
		tx.append(time())
		
		# update perm
		if verbose: print('perm',[list(perm[i]) for i in active])
		for a in active:
			perm[a][perm[a]>p_dec+1] -= p_dec
			for i in input:
				if not perm[a][i]: continue # skip unconnectable
				perm[a][i] = min(255,perm[a][i]+p_dec+p_inc)
		if verbose: print('perm',[list(perm[i]) for i in active])
		tx.append(time())
		
		# update conn
		if update_conn:
			if verbose: print('conn',[list(conn[i]) for i in range(n)])
			for a in active:
				conn[a].clear()
				conn_a = np.nonzero(perm[a]>=t)[0] # connect synapses above threshold
				conn[a].update(conn_a)
			if verbose: print('conn',[list(conn[i]) for i in range(n)])
		tx.append(time())
		
		if show_times:
			for label,t1,t0 in zip(['score','boost','activate','record activity','update perm','update conn'],tx[1:],tx):
				self.time('- '+label,t0,t1)
	
	# ---[ UTILS ]--------------------------------------------------------------
	
	@staticmethod
	def time(label,t0,t1=None):
		"print execution time"
		dt = time()-t0 if t1==None else t1-t0
		print("{:.3f}\t{}".format(dt,label))
	
	def agg_score(self,input):
		"calculate aggregated score"
		k = self.cfg['k']
		score = self.score(input)
		top = nlargest(k,score.values())
		q1 = top[k//4]
		q2 = top[k//2]
		q3 = top[k*3//4]
		return dict(
			min=min(top),
			max=max(top),
			q1=q1,q2=q2,q3=q3,
			pct_min=1.0*min(top)/k,
			pct_max=1.0*max(top)/k,
			pct_q1=1.0*q1/k,
			pct_q2=1.0*q2/k,
			pct_q3=1.0*q3/k,
			k=k)
	
	def agg_activity(self):
		"calculate aggregate stats od neuron activity"
		k = self.cfg['k']
		n = self.cfg['n']
		activity = self.activity
		cycles = self.cycles
		top = sorted(activity.flatten().tolist(),reverse=True)
		q1 = int(top[n//4])
		q2 = int(top[n//2])
		q3 = int(top[n*3//4])
		nonzero = activity[activity>0]
		gtz = nonzero.size
		nonzero_q1 = top[gtz//4]
		nonzero_q2 = top[gtz//2]
		nonzero_q3 = top[gtz*3//4]
		nonzero_min = nonzero.min()
		return dict(
			nonzero_cnt = gtz,
			nonzero_avg = 1.0 * activity.sum() / gtz,
			nonzero_q1 = nonzero_q1,
			nonzero_q2 = nonzero_q2,
			nonzero_q3 = nonzero_q3,
			nonzero_min = nonzero_min,
			zero_cnt = n-gtz,
			max = max(activity),
			min = min(activity),
			q1=q1,q2=q2,q3=q3,
			cycles=cycles,
			n=n)
	
	def agg_perm(self):
		"calculate aggregate stats of synaptic permanence"
		t = self.cfg['t']
		n = self.cfg['n']
		m = self.cfg['m']
		k = self.cfg['k']
		u = self.cfg['u']
		p_dec = self.cfg['p_dec']
		perm = self.perm
		conn = self.conn
		#
		total = m*n
		above_cnt = perm[perm>=t].size
		nonzero_cnt = perm[perm>0].size
		zero_cnt = perm[perm==0].size
		max_cnt = perm[perm==255].size
		min_cnt = perm[perm<=p_dec].size
		conn_top = sorted([len(conn[i]) for i in range(n)],reverse=True)
		conn_cnt = sum(conn_top)
		conn_cnt_min = min(conn_top)
		conn_cnt_max = max(conn_top)
		conn_cnt_q1 = conn_top[n//4]
		conn_cnt_q2 = conn_top[n//2]
		conn_cnt_q3 = conn_top[n*3//4]
		conn_sum = sum([perm[i][list(conn[i])].sum() for i in range(n)])
		conn_avg = 1.0 * conn_sum / conn_cnt
		all_sum = perm.sum()
		all_avg = 1.0 * all_sum / total
		nonzero_avg = 1.0 * all_sum / nonzero_cnt
		return dict(
			above_cnt = above_cnt,
			nonzero_cnt = nonzero_cnt,
			zero_cnt = zero_cnt,
			max_cnt = max_cnt,
			min_cnt = min_cnt,
			conn_cnt = conn_cnt,
			conn_cnt_min = conn_cnt_min,
			conn_cnt_max = conn_cnt_max,
			conn_cnt_q1 = conn_cnt_q1,
			conn_cnt_q2 = conn_cnt_q2,
			conn_cnt_q3 = conn_cnt_q3,
			total = total,
			conn_avg = conn_avg,
			all_avg = all_avg,
			nonzero_avg = nonzero_avg,
			t=t,k=k)
