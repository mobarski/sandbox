from __future__ import print_function
import numpy as np

from random import randint,shuffle
from time import time
import marshal
from heapq import nlargest # not used

# TODO different size of input and pooler

# TODO better boost_factor formula
# TODO permanence of overlap as tie-breaker in overlap score
# TODO better p_inc p_dec formula

# TODO visualization

# TODO numba
# TODO numba+cuda

# TODO multiprocessing .learn
# TODO multiprocessing .score
# TODO multiprocessing .init

# TODO sparsify .perm
# TODO sequence prediction

def random_sdr(n,w):
	w = w if type(w)==int else int(w*n)
	out = set(np.random.randint(0,n,w))
	while len(out)<w:
		out.add(randint(0,n-1))
	return out

class spatial_pooler:
	def __init__(self, n, w, t=200,
					boost=True, b_min=0.75, b_max=1.25,
					p_inc=10, p_dec=10 ):
		"""
		Parameters
		----------
			n - number of neurons
			w - number of neurons to fire
			t - connection threshold
			boost - 
			b_min - 
			b_max - 
			p_inc - 
			p_dec - 
		"""
		self.cfg = {}
		self.cfg['n'] = n
		self.cfg['w'] = w if type(w)==int else int(w*n) # TODO DOC
		self.cfg['t'] = t
		self.cfg['p_inc'] = p_inc
		self.cfg['p_dec'] = p_dec
		self.cfg['b_min'] = b_min
		self.cfg['b_max'] = b_max
		self.cfg['boost'] = boost
		self.conn = {x:random_sdr(n,w) for x in range(n)} # TODO optimize
		self.activity = np.zeros(n,dtype=np.uint32)
		self.cycles = 0
		self.perm = None # synaptic permanence
		self._init_perm()

	def _init_perm(self):
		"initialize synaptic permanence values"
		t = self.cfg['t']
		n = self.cfg['n']
		w = self.cfg['w']
		conn = self.conn
		
		perm = np.random.randint(1,t-1,(n,n),np.uint8)
		for i in range(n):
			perm[i][list(conn[i])] = np.random.randint(t,255,w)
		self.perm = perm

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
		
	# ----------------------------------------------------------------------
	
	def score(self,input):
		"calculate overlap score for every neuron"
		conn = self.conn
		score = {x:len(input & conn[x]) for x in conn}
		return score
	
	def learn(self,input,update_conn=True,verbose=False,show_times=False):
		"learn single input"
		
		w = self.cfg['w']
		n = self.cfg['n']
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
			target_pct = 1.0 * w / n # uniform distribution
			cycles = self.cycles or 1
			for i in score:
				activity_pct = 1.0 * activity[i] / cycles
				boost_factor = b_max if activity_pct < target_pct else b_min+(1.0-b_min)*target_pct/activity_pct # TODO
				score[i] *= boost_factor
		tx.append(time())
		
		# activate
		by_score = sorted(score.items(),key=lambda x:x[1],reverse=True)
		active = [x[0] for x in by_score[:w]]
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
				perm[a][i] = min(255,perm[a][i]+p_dec+p_inc)
		if verbose: print('perm',[list(perm[i]) for i in active])
		tx.append(time())
		
		# update conn
		if update_conn:
			if verbose: print('conn',[list(conn[i]) for i in range(n)])
			for a in active:
				conn[a].clear()
				conn[a].update(perm[a].argsort()[-w:])
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
		