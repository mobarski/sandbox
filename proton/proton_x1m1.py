from __future__ import print_function

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


# TODO wybrac konwencje
# czy kolekcja:zadanie:kolejka -> test:crawler:todo
# czy zadanie:kolekcja:kolejka -> crawler:test:todo
# czy zadanie:kolejka:kolekcja -> crawler:todo:test
def keyname(app,col,queue):
	return ':'.join([col,app,queue])

# why exec and not just normal decorator?
# normal decorator doesn't work -> function cannot be serialized with cPickle
# executing source code work ok but we have to be careful with imports
def pool_init(fun_name, fun_src, todo, error):
	exec(fun_src)
	exec("globals()['f'] = "+fun_name)
	exec("globals()['todo'] = '{0}'".format(todo))
	exec("globals()['error'] = '{0}'".format(error))
def wrapped(col):
	app = ''
	try:
		app = f.__name__ # TODO
		in_key = keyname(app, col, 'todo')
		id = db.spop(in_key)
		if id is None: return 'none'
		resp = f(id)
		resp_key = keyname(app, col, resp)
		db.sadd(resp_key, id)
		return resp
	except Exception as e:
		# TODO handle exception with app key
		er_key = keyname(app, col, 'error')
		db.sadd(er_key,id)
		info = {} # TODO time, exception, f
		ser_info = str(e) # TODO, stack trace, locals
		ex_key = keyname(app, col, 'exception')
		db.hset(ex_key, id, ser_info)
		return 'error'


class proton:
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
	db = redis.StrictRedis('127.0.0.1')
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
	p = proton('echo',db,2)
	resp = p.loop(handler2, 'todo', ['test']*4)
	print(resp['summary'])
	#print(db.keys())
	#for k,v in db.hscan_iter('test:exception:handler2'):
	#	print(k,v)

