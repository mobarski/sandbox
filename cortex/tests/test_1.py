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

	if 0:
		N = 128*128
		W = N//50
		#N = 64
		#W = 8
		a = random_sdr(N,W)
		t0=time()
		sp = spatial_pooler(N,W,t=100)
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
		#print(sp.activity)


	if 0:
		t0=time()
		sp = spatial_pooler.load(open('sp_test.marshal','rb'))
		sp.time('load',t0)
		n = sp.cfg['n']
		w = sp.cfg['w']
		t0=time()
		for _ in range(200):
			a = random_sdr(n,w)
			sp.learn(a)
		sp.time('learn',t0)
		print(sp.activity)
		print(sum(sp.activity))
		

	if 0:
		N = 16
		W = 2
		sp = spatial_pooler(N,W,boost=True)
		X = [random_sdr(N,W) for _ in range(4)]
		for _ in range(10):
			for x in X:
				sp.learn(x)
		print(sp.activity)
		print(sum(sp.activity))

	if 1:
		N = 8
		W = 3
		sp = spatial_pooler(N,W,boost=True,b_min=0.1)
		x = random_sdr(N,W)
		for _ in range(20):
			sp.learn(x,verbose=True)
		print()
		print(sp.activity)
	