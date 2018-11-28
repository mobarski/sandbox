import numpy as np
from random import shuffle
from time import time
import marshal
from heapq import nlargest

# REFERENCES:
## https://www.quantamagazine.org/new-ai-strategy-mimics-how-brains-learn-to-smell-20180918/
## http://science.sciencemag.org/content/sci/358/6364/793.full.pdf


# TODO - FEATURES:
## negative connections - jak nie bedzie w in to trafia do neg, jak znowu nie bedzie to wypada

# TODO - OPTIMIZE:
## score - multiprocessing
## score - numba
## score - numba+cuda

def combinations(n,k):
	k = k if type(k)==int else int(k*n)
	if k < 0.3*n: # TODO - optimize threshold
		out = set(np.random.randint(0,n,k))
		while len(out)<k:
			missing_cnt = k-len(out)
			out.update(np.random.randint(0, n, missing_cnt))
	else:
		out = list(range(n))
		shuffle(out)
		return set(out[:k])
	return out

def random_vector(lo,hi,n):
	return np.random.randint(lo,hi,n)

def random_sparse_vector(lo,hi,n,d=0.1):
	sparse = np.zeros(n)
	k = int(d*n)
	positions = combinations(n,k)
	sparse[list(positions)] = random_vector(lo,hi,k)
	return sparse 

def clock(label,t0,t1=None):
	"print execution time"
	dt = time()-t0 if t1==None else t1-t0
	print("{:.3f}\t{}".format(dt,label))

def dict_top(d,k):
	return nlargest(k,d,key=lambda x:d[x])

# ------------------------------------------------------------------------------

class onn_layer:
	"""
	Olfaction based Sparse/Random Neural Network with binary weights and k-winners
	"""
	def __init__(self, n_in, n_out, density=1.0, p_lo=10, p_hi=100):
		self.cfg = {}
		self.cfg['n_in'] = n_in
		self.cfg['n_out'] = n_out
		self.cfg['n_conn'] = int(density*n_in)
		self.cfg['p_lo'] = p_lo
		self.cfg['p_hi'] = p_hi
		self.cfg['density'] = density # remove ???
		self.conn = None # [i_out] -> set([i_in...])
		self.perm = None # [i_out][i_in] -> connection permanence
		self.init()
	
	def init(self):
		cfg = self.cfg
		n_conn = cfg['n_conn']
		n_out = cfg['n_out']
		n_in = cfg['n_in']
		p_lo = cfg['p_lo']
		p_hi = cfg['p_hi']
		
		# conn
		conn = {}
		for i in range(n_out):
			conn[i] = combinations(n_in, n_conn)
		self.conn = conn
		
		# perm
		if 0:
			perm = {}
			for i in conn:
				perm[i] = {j:p for j,p in zip(conn[i],random_vector(p_lo, p_hi, n_conn))}
			self.perm = perm
		else:
			perm = np.zeros((n_out,n_in),np.uint8)
			for i in conn:
				perm[i][list(conn[i])] = random_vector(p_lo, p_hi, n_conn)
			self.perm = perm
	
	def save(self,f):
		version = 2
		p0 = f.tell()
		marshal.dump(self.cfg,  f, version)
		marshal.dump(self.conn, f, version)
		if 0:
			marshal.dump(self.perm, f, version)
		else:
			self.perm.tofile(f)
		return f.tell()-p0
	
	@staticmethod
	def load(f):
		pass # TODO
	
	# ---[ CORE ]---------------------------------------------------------------
	
	def score(self, input):
		conn = self.conn
		score = {}
		for i in conn:
			score[i] = input[list(conn[i])].sum()
		return score
	
	def learn(self, input, k, p_inc=10, p_dec=5, p_min=20, p_lo=21, p_hi=40):
		cfg = self.cfg
		conn = self.conn
		perm = self.perm
		n_in = cfg['n_in']
		n_conn = cfg['n_conn']
		# score
		score = self.score(input)
		# k winners take all
		winners = dict_top(score, k)
		for w in winners:
			# update perm
			avg = 1.0*score[w]/n_conn
			for i in conn[w]:
				perm[w][i] += p_inc if input[i] else -p_dec
				# TODO TEST only x best inputs improves perm
				# TODO TEST only x random inputs improves perm
				# TODO TEST only inputs above average improves perm, x random below average degrades perm
			# remove conn
			old = perm[w][perm[w]<p_min].nonzero()[0].tolist()
			perm[w][old] = 0
			conn[w].difference_update(old)
			# add new conn
			if old:
				new = set(combinations(n_in,len(old)))
				new.difference_update(conn[w])
				perm[w][list(new)] = random_vector(p_lo,p_hi,len(new))
				conn[w].update(new)
	
if __name__=="__main__":
	t0=time()
	n=128
	nn=onn_layer(n*n,n*n,0.02)
	clock('init',t0)
	#print(nn.conn[0])
	#print(nn.perm[0])
	t0=time()
	x=nn.save(open('data_v1.marshal','wb'))
	clock('save',t0)
	print(x)
	input = random_sparse_vector(100,200,n*n,0.02)
	t0=time()
	s = nn.score(input)
	clock('score',t0)
	#print(s)
	t0=time()
	nn.learn(input,100)
	clock('learn',t0)
	