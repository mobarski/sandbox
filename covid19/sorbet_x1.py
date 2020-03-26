from sorbet import sorbet

from concurrent.futures import ThreadPoolExecutor as TPool
from concurrent.futures import ProcessPoolExecutor as PPool
from itertools import chain
class xsorbet(sorbet):
	def scan(self, fun, n, pool):
		#with TPool(max_workers=n) as pool:
		#	results = pool.map(fun, self)
			#yield from chain.from_iterable(results)
		#return chain.from_iterable(results)
		results = pool.map(fun, self)
		return filter(bool,results)

	def batch1(self, n):
		return [(self.path,list(range(x,x+n))) for x in range(0,len(self),n)]

	def batch2(self, n):
		return [(self.path,x,x+n) for x in range(0,len(self),n)]

def worker0(val):
	return val['a']*11

def worker1(args):
	db_path,ids = args
	db = sorbet(db_path).load()
	out = []
	for id in ids:
		val = db[id]
		out += [val['a']*11]
	return out

def worker2(args):
	path,lo,hi = args
	db = sorbet(path).load()
	out = []
	for val in db[lo:hi]:
		out += [val['a']*11]
	return out

if __name__=="__main__":
	from time import time
	import sys
	label = sys.argv[0][:-3]
	path = f'data/sorbet'
	
	db = xsorbet(path).load()
	
	# 61s
	import multiprocessing as mp
	if 0:
		t0=time()
		with mp.Pool(processes=4) as pool:
			N = 1000
			ids = [list(range(x,x+N)) for x in range(0,len(db),N)]
			#print('ids',ids)
			results = pool.map(worker1,zip([path]*len(ids),ids))
			#print(results)
		print(time()-t0)

	
	if 0:
		t0=time()
		#with mp.Pool(processes=4) as pool:
		with PPool(max_workers=4) as pool: # 71s
			args = db.batch1(1000)
			#print(args)
			results = pool.map(worker1, args)
		print(time()-t0)

	
	if 0:
		t0=time()
		with mp.Pool(processes=4) as pool: # 60s
		#with PPool(max_workers=4) as pool: # 68s
			args = db.batch2(1000)
			print(args)
			results = pool.map(worker2, args)
		print(time()-t0)

	# 63s
	if 0:
		t0=time()
		with PPool(max_workers=4) as pool:
			N = 1000
			ids = [list(range(x,x+N)) for x in range(0,len(db),N)]
			#print('ids',ids)
			results = pool.map(worker1,zip([path]*len(ids),ids))
			#print(results)
		print(time()-t0)

	t0=time()
	if 1:
		# 3.5s
		for x in map(worker0, db):
			pass
	if 0:
		# 5s
		with mp.Pool(processes=4) as pool:
			results = pool.map(worker0,db)
	if 0:
		# 53s -> mem problem
		with TPool(max_workers=4) as pool:
			results = pool.map(worker0,db)
	if 0:
		# 
		with PPool(max_workers=4) as pool:
			results = pool.map(worker0,db)
	print(time()-t0)
