import numpy as np

from random import randint,shuffle
from time import time
import marshal
from heapq import nlargest # not used

# TODO activity statistics
# TODO boosting
# TODO different size of input and pooler

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
	def __init__(self,n,w,t=200):
		"""
		Parameters
		----------
			n - number of neurons
			w - number of neurons to fire
			t - activation threshold
		"""
		self.cfg = {}
		self.cfg['n'] = n
		self.cfg['w'] = w if type(w)==int else int(w*n) # TODO DOC
		self.cfg['t'] = t
		self.cfg['p_inc'] = 10
		self.cfg['p_dec'] = 10
		t0 = time()
		self.conn = {x:random_sdr(n,w) for x in range(n)} # TODO optimize
		print('init0',time()-t0)
		self.perm = None
		self._init_perm()

	@staticmethod
	def load(f):
		self = spatial_pooler(0,0)
		self.cfg = marshal.load(f)
		self.conn = marshal.load(f)
		n = self.cfg['n']
		self.perm = np.fromfile(f,np.uint8).reshape((n,n))
		return self

	def save(self,f,version=2):
		marshal.dump(self.cfg, f, version)
		marshal.dump(self.conn, f, version)
		self.perm.tofile(f)

	def _init_perm(self):
		t = self.cfg['t']
		n = self.cfg['n']
		w = self.cfg['w']
		conn = self.conn
		
		t0 = time()
		perm = np.random.randint(1,t-1,(n,n),np.uint8)
		print('init1',time()-t0)
		t0 = time()
		for i in range(n):
			perm[i][list(conn[i])] = np.random.randint(t,255,w)
		print('init2',time()-t0)
		self.perm = perm
		
	
	# overlap score
	def score(self,input):
		conn = self.conn
		score = {x:len(input & conn[x]) for x in conn}
		return score
	
	def learn(self,input,update_conn=True):
		w = self.cfg['w']
		n = self.cfg['n']
		p_inc = self.cfg['p_inc']
		p_dec = self.cfg['p_dec']
		conn = self.conn
		perm = self.perm
		
		tx=[]
		
		# score
		tx.append(time())
		score = self.score(input)
		
		# activate
		tx.append(time())
		by_score = sorted(score.items(),key=lambda x:x[1],reverse=True)
		active = [x[0] for x in by_score[:w]]
		tx.append(time())
		##print('input',input)
		##print('active',active)
		
		# update perm
		##print('perm',perm)
		for a in active:
			perm[a][perm[a]>p_dec+1] -= p_dec
			for i in input:
				perm[a][i] = min(255,perm[a][i]+p_dec+p_inc)
		##print('perm',perm)
		tx.append(time())
		
		# update conn
		if update_conn:
			##print('conn',conn)
			for a in active:
				conn[a].clear()
				conn[a].update(perm[a].argsort()[-w:])
			##print('conn',conn)
		tx.append(time())
		
		for label,t1,t0 in zip(['score','activate','udate perm','update conn'],tx[1:],tx):
			print(label,t1-t0)


if __name__=="__main__":
	if 0:
		a = random_sdr(16,8)
		b = random_sdr(16,8)
		print(a)
		print(b)
		print(a&b)
		print(a|b)
		print(a^b)

	if 0:
		a = random_sdr(16,8)
		b = random_sdr(16,8)
		sp = spatial_pooler(16,4,t=100)
		print(sp.conn)
		print(sp.score(a))
		sp.init_perm()
		print(sp.perm)
		sp.learn(a)
		sp.learn(b)

	if 1:
		N = 128*128
		W = N//50
		a = random_sdr(N,W)
		t0=time()
		sp = spatial_pooler(N,W,t=100)
		print('init',time()-t0)
		t0=time()
		sp.learn(a)
		print('learn',time()-t0)
		t0=time()
		sp.score(a)
		print('score',time()-t0)
		t0=time()
		sp.save(open('sp_test.marshal','wb'))
		print('save',time()-t0)


	if 1:
		t0=time()
		sp = spatial_pooler.load(open('sp_test.marshal','rb'))
		print('load',time()-t0)
		N = sp.cfg['n']
		W = sp.cfg['w']
		a = random_sdr(N,W)
		t0=time()
		sp.learn(a)
		print('learn',time()-t0)
