from __future__ import print_function

from multiprocessing import Pool
from itertools import izip_longest
from collections import Counter
from inspect import getsource
from textwrap import dedent
from time import time,sleep

import redis
import sys
import re

def grouper(iterable, n):
	"""
	>>> list(grouper(range(10),3))
	[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
	"""
	it = iter(iterable)
	for group in izip_longest(*[it]*n):
		yield [x for x in group if x is not None]


# TODO inna kolejnosc argumentow aby latwiej robic partial?
# TODO krotsza nazwa?
# TODO wybrac konwencje
# czy kolekcja:zadanie:kolejka -> test:crawler:todo
# czy zadanie:kolekcja:kolejka -> crawler:test:todo
# czy zadanie:kolejka:kolekcja -> crawler:todo:test
def keyname(app,col,queue):
	return ':'.join([col,app,queue])

# why exec and not just normal decorator?
# normal decorator doesn't work -> function cannot be serialized with cPickle
# executing source code work ok but we have to be careful with imports
def pool_init(fun_name, fun_src, init_name='',init_src='',init_args=[]):
	if init_name:
		exec(init_src)
		exec(init_name+"(*init_args)")
	exec(fun_src)
	exec("globals()['f'] = "+fun_name)
def wrapped(col): # TODO rename
	app = ''
	try:
		app = f.__name__ # TODO app name???
		in_key = keyname(app, col, 'todo')
		id = db.spop(in_key)
		
		# TODO pozwolic obsluzyc to w funkcji
		#      aby mozna bylo robic zadana generujace idki?
		#      wtedy tez warto by bylo zwracac jakis counter ile dodano
		#  CZY takie generatory obsluzymy w specjalny sposob?
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
	
	def loop(self, handler, collection_list, init=None, init_args=[]):
		t0 = time()
		fun_name = handler.__name__
		fun_src = dedent(getsource(handler))
		if init:
			init_name = init.__name__
			init_src = dedent(getsource(init))
			
			# export local variables as globals
			last_line = init_src.rstrip().split('\n')[-1]
			indent = re.findall('^\s+',last_line)[0]
			init_src += indent + "for __k,__v in locals().items(): globals()[__k]=__v"
			
		else:
			init_name = ''
			init_src = ''
		pool_args = [fun_name, fun_src, init_name, init_src, init_args]
		t1 = time()
		pool = Pool(self.workers, pool_init, pool_args, self.reset_after)
		t2 = time()
		results = pool.map(wrapped, collection_list)
		t3 = time()
		status = dict(Counter(results))
		t4 = time()
		return {'t_init':t2-t1,'t_total':t4-t0,'t_fun':t3-t2,'status':status,'count':len(collection_list)} # TODO more stats


db = redis.StrictRedis('127.0.0.1')
if __name__=="__main__":
	#db = redis.StrictRedis('127.0.0.1')
	col = 'test'
	app = 'handler2'
	db.sadd(keyname(app,col,'all'),'a','b','c','d','e','f','g','h','i','j','k','l','m','n')
	db.delete(keyname(app,col,'done'))
	db.sdiffstore(keyname(app,col,'todo'),keyname(app,col,'all'),keyname(app,col,'done'))
	
	# --------------------------------------------------
	## def init():
		## db = redis.StrictRedis('127.0.0.1')
	def handler2(id):
		print('handling id',id); sys.stdout.flush()
		#x=1/0
		sleep(1)
		return 'done'
	p = proton('echo',db,2)
	resp = p.loop(handler2, ['test']*4)
	print(resp)
