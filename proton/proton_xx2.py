import redis
from multiprocessing import Pool
from time import time
from collections import Counter

def wrapped(fun,db):
	def f(col):
		id = db.spop(col+':todo')
		if id is None: return 'none'
		resp = fun(id)
		db.sadd(col+':'+resp,id)
		return resp
	return f

class proton:
	def __init__(self, db, workers, reset_after=None):
		self.db = db
		self.workers = workers
		self.pool = Pool(workers,None,[],reset_after)
	
	def loop(self, fun, collection_list):
		t0 = time()
		handler = wrapped(fun,self.db)
		summary = Counter(self.pool.map(handler,collection_list))
		return {'summary':summary}
