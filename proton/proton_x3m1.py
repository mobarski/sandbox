from __future__ import print_function

"""
PROTON - simple parallel batch processing coordinator with status persistance
"""

# CHANGELOG
# - 2018-10-04: batch(f,n=100), get_ids(status,n), add_ids(status,ids), delete_except

# TODO
# - stats
# - built on top: map/combine/reduce

from itertools import groupby
from multiprocessing import Pool
import os

class proton:
	def __init__(self,
			db=None, # redis connection
			workers=4,
			worker_init=None,
			worker_init_args=None,
			worker_max_batches=None,
			stop=['stop']
			):
		self.db = db
		self.workers = workers
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
	
	def batch(self,fun,n=100):
		self.check_stop()
		# TODO init stats
		ids = self.get_ids('todo',n)
		results = self.pool.map(fun,ids)
		return results
	
	def check_stop(self):
		for path in self.stop:
			if os.path.exists(path):
				raise Exception('Stop file detected: {}'.format(path))

	def update(self, results):
		"update item status from results"
		results.sort(key=lambda x:x[1])
		for status,grouped in groupby(results,lambda x:x[1]):
			ids = [x[0] for x in grouped]
			self.add_ids(status, ids)
		# TODO save stats
	
	def restart(self):
		src = self.all
		dst = self.col+':todo'
		self.add_col(src,dst)
	
	def count(self,status):
		if status=='all':
			target = self.all
		else:
			target = self.col + ':' + status
		return self.cardinality(target)
		
	
	# --- DATABASE ACCESS---------------------------------------------------
	
	def add_ids(self, status, ids):
		"add ids to focus:status collection"
		col = self.col+':'+status
		self.db.sadd(col,*ids)
		
	def get_ids(self, status, n):
		"pop n ids from focus:status collection"
		col = self.col+':'+status
		ids = self.db.spop(col, n)
		return ids
	
	def add_col(self, src, dst):
		"add src collection to dst collection"
		self.db.sunionstore(dst,dst,src)
		
	def cardinality(self, col):
		"return number if ids in collection"
		return self.db.scard(col)

	def delete(self, *status):
		"delete given statuses from collection in focus"
		for s in status:
			self.db.delete(self.col+':'+s)
	
	# TODO rename to "keep" ???
	def delete_except(self, *status):
		"delete statuses from collection in focus except for given"
		prefix_len = len(self.col+':')
		to_del = []
		for col in self.db.keys(self.col+':*'):
			s = col[prefix_len:]
			if ':' in s: continue # prevent mistakes
			if s not in status: to_del.append(col)
		if to_del:
			self.db.delete(*to_del)

# ----------------------------------------------------------------------

if __name__=="__main__":
	from db import db
	
	def test_fun(id):
		return id,'done',{'val':'ok'+str(id)}	

	pool = proton(db,stop=['stop.proton'])

	pool.focus('proton:test')
	#pool.delete('done')
	#pool.add_ids('all',range(1000))
	#pool.restart()

	if 1:
		results = pool.batch(test_fun,100)
		for id,status,value in results:
			print(id,value)
		pool.update(results)
		
	print('all',pool.all,pool.count('all'))
	print('todo',pool.count('todo'))
	print('done',pool.count('done'))
	pool.delete_except()
	
