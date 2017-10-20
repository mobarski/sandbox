from __future__ import print_function

# TODO wybrac konwencje -- szybka podmiana jednej funkcji
# czy kolekcja:zadanie:kolejka -> test:crawler:todo
# czy zadanie:kolekcja:kolejka -> crawler:test:todo
# czy zadanie:kolejka:kolekcja -> crawler:todo:test

import redis
import json
from traceback import format_exc
from multiprocessing import Pool
from collections import Counter
from inspect import getsource
from textwrap import dedent
from time import time

def pool_init(fun_name, fun_src, label):
	exec(fun_src)
	exec("globals()['f'] = "+fun_name)
	f.__label__ = label or fun_name
def wrapped(col):
	try:
		id = db.spop(col+':todo')
		if id is None: return 'none'
		resp = f(id)
		db.sadd(col+':'+resp,id)
		return resp
	except Exception as e:
		db.sadd(col+':error',id)
		info = {'msg':str(e), 'time':time(), 'traceback':format_exc(e)} # TODO time, exception, f, stack trace, locals
		ser_info = json.dumps(info)
		ex_key = col+':exception:'+f.__label__
		db.hset(ex_key, id, ser_info)
		return 'error'


class proton:
	def __init__(self, db, workers, reset_after=None):
		self.db = db
		self.workers = workers
		self.reset_after = reset_after
	
	def loop(self, fun, collection_list, label=''):
		fun_src = dedent(getsource(fun))
		t0 = time()
		pool_init_args = [fun.__name__, fun_src, label]
		pool = Pool(self.workers, pool_init, pool_init_args, self.reset_after)
		summary = Counter(pool.map(wrapped, collection_list))
		dt = time()-t0
		return {'dt':dt,'summary':summary} # TODO more stats


if __name__=="__main__":
	from time import sleep
	db = redis.StrictRedis('localhost')
	col = 'test'
	db.sadd(col+':all','a','b','c','d','e','f','g','h','i','j','k','l','m','n')
	db.delete(col+':done')
	db.sdiffstore(col+':todo',col+':all',col+':done') # budowa TODO
	
	aux_dict = dict(a=0,b=2,c=3,d=4,e=5,f=6,g=7,h=9,i=10,j=11,k=12,l=13,m=14,n=15)
	
	# --------------------------------------------------
	def handler2(id):
		print('handling id',id,'out',aux_dict[id],len(db.keys()))
		x=1/0
		sleep(1)
		return 'done'
	p = proton(db,2)
	resp = p.loop(handler2, ['test']*4)
	print(resp['summary'])
	## print(db.keys())
	for k,v in db.hscan_iter('test:exception:handler2'):
		print(k,v)

