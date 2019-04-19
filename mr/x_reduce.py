import sqlite3
from time import time

# TODO python combiner
# TODO python combiner union
# TODO grouping
# TODO parameter placeholders

def _map_fun(sql, part, path, combiner, functions, aggregates):
	t0=time()
	db = sqlite3.connect(path)
	
	for x in functions:
		db.create_function(*x)
	for x in aggregates:
		db.create_aggregate(*x)
	
	result = db.execute(sql)
	out = {}
	out['rows'] = list(result)
	out['cols'] = [x[0] for x in result.description]
	out['part'] = part
	out['map_time'] = time()-t0
	if combiner:
		t0=time()
		out = combiner(out)
		out['combine_time'] = time()-t0
	return out


def _map_fun1(args):
	return _map_fun(*args)


def map_sql(sql, parts, path_fun, pool=None, combiner=None, functions=[], aggregates=[]):
	args = [(sql,part,path_fun(part),combiner,functions,aggregates) for part in parts]
	if pool:
		out = pool.map(_map_fun1, args)
	else:
		out = map(_map_fun1, args)
	return out


def union(map_output):
	tab = 'part' # TODO rename ???
	cols = map_output[0]['cols']
	db=sqlite3.connect(':memory:')
	db.execute('create table {}({})'.format(tab, ','.join(cols)))
	for p in map_output:
		sql = 'insert into {} values({})'.format(tab, ','.join(['?']*len(cols)))
		db.executemany(sql,p['rows'])
	return db

def reduce_sql(sql, map_output):
	db = union(map_output)
	return db.execute(sql)

# ------------------------------------------------------------------------------

if __name__=="xxx__main__":
	import multiprocessing as mp
	pool = mp.Pool(2)

	def get_part_path(part):
		return '../data/unamo/bb/tab/{}'.format(part)

	out = map_sql("""
			select category_name, day, count(1) as count
			from raw
			group by category_name, day
		"""
		,['20190316','20190317','20190318']
		,get_part_path
		,pool=pool
		)

	for x in reduce_sql("""
				select day, sum(count) as count
				from part group by day
				order by count desc
			""", out
			):
		print(x)


# ------------------------------------------------------------------------------

from marshal import dumps,loads
#from pickle import dumps,loads
from collections import Counter
import re


def tf(map_fun_output):
	out = map_fun_output
	
	tf = Counter()
	for row in out['rows']:
		tokens = re.findall('(?u)\w+',row[0])
		tf.update(tokens)
	if 1:
		out['cols'] = ['group','tf']
		out['rows'] = [('all',dict(tf))]
	else:
		out['cols'] = ['term','freq']
		out['rows'] = tf.items()
	return out

class TF:
	def __init__(self):
		self.tf = Counter()
	def step(self, value):
		tokens = re.findall('(?u)\w+',value)
		self.tf.update(tokens)
	def finalize(self):
		return buffer(dumps(dict(self.tf)))

if __name__=="__main__":	
	import multiprocessing as mp
	pool = mp.Pool(2)
	
	def get_part_path(part):
		return '../data/unamo/bb/tab/{}'.format(part)

	out = map_sql("""
			select lower(content_message)
			from raw
			where category_name=='twitter'
			limit 100
		"""
		,['20190317']
		,get_part_path
		,combiner=tf
		,pool=pool
		)
	print(out)

	if 0:
		out = map_sql("""
				select tf(lower(content_message)) as tf
				from raw
				where category_name=='twitter'
			"""
			,['20190317']
			,get_part_path
			,aggregates=[('tf',1,TF)]
			,pool=pool
			)
		tf = loads(out[0]['rows'][0][0])
		print(tf)


