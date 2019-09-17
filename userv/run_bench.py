import requests
import multiprocessing as mp
from time import time

N=2000
W=10

def bench(i):
	_i = str(i)
	requests.get('http://127.0.0.1:8080/kv',params=dict(op='set',k='k'+_i,v='v'+_i))

if __name__=="__main__":
	pool = mp.Pool(W)
	t0=time()
	pool.map(bench,range(N))
	dt=time()-t0
	print(dt,1.0*N/dt)
