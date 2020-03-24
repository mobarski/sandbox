import h5py
import json
from pickle import dumps,loads

N = 1000
f = h5py.File('data/h5.data','w')
dt = h5py.string_dtype()
db = f.create_dataset("name", (N,), dtype=dt)

if __name__=="__main__":
	from time import time
	if 1:
		t0=time()
		for i in range(N):
			db[i] = dumps({'a':1,'aa':11},0)
		print("write time:",f"{time()-t0:.02f}s",f'{N/(time()-t0):.0f} items/s')
	if 0:
		db = DB('data/v1')
		t0=time()
		for i in range(N):
			db[i]
		print("read time:",f"{time()-t0:.02f}s",f'{N/(time()-t0):.0f} items/s')
