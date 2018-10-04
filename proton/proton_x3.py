from __future__ import print_function

from itertools import groupby
from multiprocessing import Pool
import os

class proton:
	def __init__(self,
			db=None, # redis connection
			workers=4,
			per_worker=100,
			worker_init=None,
			worker_init_args=None,
			worker_max_batches=None,
			stop=['stop']
			):
		self.db = db
		self.workers = workers
		self.per_worker = per_worker
		self.per_batch = workers * per_worker
		self.col = None
		self.all = None
		self.stop = stop
		# 
		self.pool = Pool(
				workers,
				worker_init,
				worker_init_args,
				worker_max_batches)
	
	def focus(self, col, all=None):
		self.col = col
		self.all = all if all else col+':all'
	
	def batch(self,fun):
		self.check_stop()
		# TODO stats
		ids = self.get_ids()
		results = self.pool.map(fun,ids)
		return results
	
	def check_stop(self):
		for path in self.stop:
			if os.path.exists(path):
				raise Exception('Stop file detected: {}'.format(path))

	def update(self, results):
		results.sort(key=lambda x:x[1])
		for status,grouped in groupby(results,lambda x:x[1]):
			ids = [x[0] for x in grouped]
			target_col = self.col + ':' + status
			self.add_ids(target_col, ids)
		# TODO stats
	
	def restart(self):
		src = self.all,
		dst = self.col+':todo'
		self.add_col(src,dst)
	
	def count(self,status):
		if status=='all':
			target = self.all
		else:
			target = self.col + ':' + status
		return self.cardinality(target)
		
	
	# --- DATABASE LAYER ---------------------------------------------------
	
	def add_ids(self, col, ids):
		#return print('ADD_IDS_TO_COL',col,ids) # DEBUG
		self.db.sadd(col,*ids)
		
	def get_ids(self):
		#return [111,222,333,444,555,666,777,888,999] # DEBUG
		todo_col = self.col+':todo'
		ids = self.db.spop(todo_col, self.per_batch)
		return ids
	
	def add_col(self, src, dst):
		self.db.sunionstore(dst,dst,src)
	
	def del_col(self, *status):
		for s in status:
			self.db.delete(self.col+':'+s)
	
	def cardinality(self, target):
		return self.db.scard(target)

# ----------------------------------------------------------------------

def crawl_one(id):
	return id,'done',dict(url='http://ok.pl',text='to jest test')

if __name__=="__main__":
	db=None
	pool = proton(db,
			workers = 4,
			per_worker = 1,
			stop = ['stop','stop.test']
		)
	pool.focus('xlink:tf',all='xlink:crawl:done')
	#iters = pool.count('todo') / self.per_batch
	for _ in range(2):
		results = pool.batch(crawl_one)
		for id,status,value in results:
			if status=='done':
				#mongo.xlink['xlink:out'].save(value)
				print('DONE',id,value)
		pool.update(results)

