from __future__ import print_function
import sys; sys.path.append('..')
from core import *

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
		K = N//50
		#N = 64
		#K = 8
		a = random_sdr(N,K)
		t0=time()
		sp = spatial_pooler(N,K,t=100)
		sp.time('init',t0)
		t0=time()
		sp.learn(a,show_times=True)
		sp.time('learn',t0)
		t0=time()
		sp.score(a)
		sp.time('score',t0)
		t0=time()
		sp.save(open('sp_test.marshal','wb'))
		sp.time('save',t0)

	if 0:
		t0=time()
		sp = spatial_pooler.load(open('sp_test.marshal','rb'))
		sp.time('load',t0)
		n = sp.cfg['n']
		k = sp.cfg['k']
		t0=time()
		for _ in range(1):
			a = random_sdr(n,k)
			sp.learn(a)
		sp.time('learn',t0)
		print(sp.activity)
		print(sum(sp.activity))
		

	if 0:
		N = 32
		K = 4
		sp = spatial_pooler(N,K,p=None,boost=True)
		X = [random_sdr(N,K) for _ in range(4)]
		for _ in range(10):
			for x in X:
				sp.learn(x,verbose=True)
		print(sp.activity)

	if 0:
		M = 16
		N = 8
		K = 3
		sp = spatial_pooler(N,K,m=M,boost=True,b_min=0.1)
		x = random_sdr(M,2)
		for _ in range(20):
			sp.learn(x,verbose=True)
		print()
		print(sp.activity)
	