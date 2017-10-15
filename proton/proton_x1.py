from __future__ import print_function

# TODO wybrac konwencje -- szybka podmiana jednej funkcji
# czy kolekcja:zadanie:kolejka -> test:crawler:todo
# czy zadanie:kolekcja:kolejka -> crawler:test:todo
# czy zadanie:kolejka:kolekcja -> crawler:todo:test

import redis
from multiprocessing import Pool
from itertools import izip_longest
from collections import Counter
from inspect import getsource
from textwrap import dedent

from time import time,sleep


def grouper(iterable, n):
	"""
	>>> list(grouper(range(10),3))
	[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
	"""
	it = iter(iterable)
	for group in izip_longest(*[it]*n):
		yield [x for x in group if x is not None]


## # TO NIE DZIALA bo nie moze spiklowac funkcji
## def wrap(f,todo='todo',error='error'):
	## def wrapped(col):
		## try:
			## id = db.spop(col+':'+todo)
			## if id is None: return 'none'
			## resp = f(id)
			## db.sadd(col+':'+resp,id)
			## return resp
		## except Exception as e:
			## db.sadd(col+':'+error,id)
			## info = {} # TODO time, exception, f
			## ser_info = ''
			## ex_key = f.__name__+':'+col+':exception'
			## db.hset(ex_key, id, ser_info)
			## return 'error'
	## return wrapped


def pool_init(fun_name, fun_src, todo, error):
	exec(fun_src)
	exec("globals()['f'] = "+fun_name)
	exec("globals()['todo'] = '{0}'".format(todo))
	exec("globals()['error'] = '{0}'".format(error))
def wrapped(col):
	try:
		id = db.spop(col+':'+todo)
		if id is None: return 'none'
		resp = f(id)
		db.sadd(col+':'+resp,id)
		return resp
	except Exception as e:
		db.sadd(col+':'+error,id)
		info = {} # TODO time, exception, f
		ser_info = str(e) # TODO, stack trace, locals
		ex_key = col+':exception:'+f.__name__ # TODO czy nazwa pliku czy nazwa poola?
		db.hset(ex_key, id, ser_info)
		return 'error'


class Proton:
	def __init__(self, name, db, workers, reset_after=None):
		self.name = name
		self.db = db
		self.workers = workers
		self.reset_after = reset_after
	
	def loop(self, handler, todo, collection_list):
		src = dedent(getsource(handler))
		t0 = time()
		pool = Pool(self.workers,pool_init,[handler.__name__,src,todo,'error'],self.reset_after)
		summary = Counter(pool.map(wrapped, collection_list))
		dt = time()-t0
		return {'dt':dt,'summary':summary} # TODO more stats


if __name__=="__main__":
	db = redis.StrictRedis('localhost')
	col = 'test'
	db.sadd(col+':all','a','b','c','d','e','f','g','h','i','j','k','l','m','n')
	db.delete(col+':done')
	db.sdiffstore(col+':todo',col+':all',col+':done') # budowa TODO
	
	# --------------------------------------------------
	def handler2(id):
		print('handling id',id)
		#x=1/0
		sleep(1)
		return 'done'
	p = Proton('echo',db,2)
	resp = p.loop(handler2, 'todo', ['test']*4)
	print(resp['summary'])
	#print(db.keys())
	#for k,v in db.hscan_iter('test:exception:handler2'):
	#	print(k,v)

