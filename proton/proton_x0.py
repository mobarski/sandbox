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


# mozliwe dwa podejscia
# a) handler dostaje id z kolekcji
# b) handler dostaje nazwe kolekcji <----
def handler(col):
	try:
		id = db.spop(col+':todo')
		if id is None: return 'empty'
		print('handling',id)
		sleep(1)
		db.sadd(col+':done',id)
		return 'done'
	except Exception as e:
		return 'error'

if __name__=="__main__":
	db = redis.StrictRedis('localhost')
	col = 'test'
	db.sadd(col+':all','a','b','c','d','e','f','g','h','i','j','k','l','m','n')
	db.delete(col+':done')
	db.sdiffstore(col+':todo',col+':all',col+':done') # budowa TODO
	
	WORKERS = 2
	PER_WORKER = 3
	TASKS = WORKERS * PER_WORKER			
	pool = Pool(WORKERS) # TODO initializer,initargs,maxtasksperchild
	
	t0 = time()
	summary = Counter(pool.map(handler, [col] * TASKS))
	dt = time()-t0
	
	done = summary.get('done',0)
	print(
		col,
		'ok {0:.0f}%'.format(100*done/TASKS),
		'dt {0:.0f}s'.format(dt),
		'done/s {0:.0f}'.format(done/dt),
		'all/s {0:.0f}'.format(TASKS/dt),
		' '.join(["{0}:{1}".format(k,v) for k,v in sorted(summary.items())]),
		sep='  '
	)

	#x = db.smembers(':todo')
	#print(x)
