import sqlite3
from time import time

# TODO explode
# TODO grouping
# TODO parameter placeholders

# NEW
import re
def regexp(expr, item):
	r = re.compile(expr,re.U)
	return r.search(item) is not None

def _map_fun(sql, part, path, combiner, functions, aggregates):
	t0=time()
	db = sqlite3.connect(path)
	
	# new
	db.create_function('regexp',2,regexp)
	
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
