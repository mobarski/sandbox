from __future__ import print_function
import numpy as np

from random import randint,shuffle
from time import time
import marshal
from heapq import nlargest

# WORK: sparsify .perm

# TODO: better boost_factor formula
# TODO: permanence of overlap as tie-breaker in overlap score
# TODO: better p_inc p_dec formula

# TODO: visualization

# TODO: numba
# TODO: numba+cuda

# TODO: multiprocessing .learn
# TODO: multiprocessing .score
# TODO: multiprocessing .init

# TODO: sequence prediction

def random_sdr(n,k):
	k = k if type(k)==int else int(k*n)
	out = set(np.random.randint(0,n,k))
	while len(out)<k:
		out.add(randint(0,n-1))
	return out

class spatial_pooler:
	def __init__(self, n, k, m=None, p=None, t=200,
					boost=True, b_min=0.75, b_max=1.25,
					p_inc=10, p_dec=6 ):
		"""
		Parameters
		----------
			n -- number of neurons (:int)
			k -- number of neurons to fire (:int) or proportion of neurons to fire (:float)
			m -- number of input neurons (equal to n by default) (:int or None)
			p -- number of possible connections per neuron (EXPERIMENTAL) ??? TODO rename to p
			t -- connection threshold (:int)
			boost -- enable overlap score boosting (:bool)
			b_min -- minimum boost factor (:int)
			b_max -- maximum boost factor (:int)
			p_inc -- permanence increase value (:int)
			p_dec -- permanence decrease value (:int)
		"""
		m = m or n
		self.cfg = {}
		self.cfg['n'] = n
		self.cfg['m'] = m
		self.cfg['k'] = int(k*n) if type(k)==float else k
		self.cfg['p'] = int(p*m) if type(p)==float else p
		self.cfg['t'] = t
		self.cfg['p_inc'] = p_inc
		self.cfg['p_dec'] = p_dec
		self.cfg['b_min'] = b_min
		self.cfg['b_max'] = b_max
		self.cfg['boost'] = boost
		self.conn = {x:random_sdr(m,k) for x in range(n)} # TODO: optimize
		self.activity = np.zeros(n,dtype=np.uint32)
		self.cycles = 0
		self.perm = None # synaptic permanence
		self._init_perm()

	def _init_perm(self):
		"initialize synaptic permanence values"
		t = self.cfg['t']
		n = self.cfg['n']
		m = self.cfg['m']
		k = self.cfg['k']
		p = self.cfg['p']
		conn = self.conn
		
		if not p:
			perm = np.random.randint(1,t-1,(n,m),np.uint8)
			for i in range(n):
				perm[i][list(conn[i])] = np.random.randint(t,255,k)
		else: # EXPERIMENTAL
			perm = {}
			for i in range(n):
				perm[i] = dict(zip(random_sdr(m,p),np.random.randint(1,255,p)))
		self.perm = perm

	@staticmethod
	def load(f):
		"load pooler from file"
		self = spatial_pooler(0,0)
		self.cfg = marshal.load(f)
		self.conn = marshal.load(f)
		self.cycles = marshal.load(f)
		n = self.cfg['n']
		self.perm = np.fromfile(f,np.uint8,n*n).reshape((n,n)) # TODO p>0
		self.activity = np.fromfile(f,np.uint32,n)
		return self

	def save(self,f,version=2):
		"save pooler to file"
		marshal.dump(self.cfg, f, version)
		marshal.dump(self.conn, f, version)
		marshal.dump(self.cycles, f, version)
		self.perm.tofile(f) # TODO p>0
		self.activity.tofile(f)
		
	## -------------------------------------------------------------------------
	
	def score(self,input):
		"calculate overlap score for every neuron"
		conn = self.conn
		score = {x:len(input & conn[x]) for x in conn}
		return score
	
	def learn(self,input,update_conn=True,verbose=False,show_times=False):
		"learn single input"
		
		k = self.cfg['k']
		p = self.cfg['p']
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
		active = [x[0] for x in by_score[:k]]
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
			if not p: # dense perm
				perm[a][perm[a]>p_dec+1] -= p_dec
				for i in input:
					perm[a][i] = min(255,perm[a][i]+p_dec+p_inc)
			else: # EXPERIMENTAL
				for i in perm[a]:
					if i in input:
						perm[a][i] = min(255,perm[a][i]+p_inc)
					else:
						perm[a][i] = max(1,perm[a][i]-p_dec)
		if verbose: print('perm',[list(perm[i]) for i in active])
		tx.append(time())
		
		# update conn
		if update_conn:
			if verbose: print('conn',[list(conn[i]) for i in range(n)])
			for a in active:
				conn[a].clear()
				if not p: # dense perm
					conn_a = perm[a].argsort()[-k:] # connect k best neurons
					# conn_a = [x for x in range(m) if perm[a][x]>=t] # TEST: connect neurons above threshold
				else: # EXPERIMENTAL
					conn_a = nlargest(k, perm[a], key=lambda x:perm[a][x]) # connect k best neurons
				conn[a].update(conn_a)
			if verbose: print('conn',[list(conn[i]) for i in range(n)])
		tx.append(time())
		
		if show_times:
			for label,t1,t0 in zip(['score','boost','activate','record activity','update perm','update conn'],tx[1:],tx):
				self.time(label,t0,t1)
	
	@staticmethod
	def time(label,t0,t1=None):
		"print execution time"
		dt = time()-t0 if t1==None else t1-t0
		print("{:.3f}\t{}".format(dt,label))
	