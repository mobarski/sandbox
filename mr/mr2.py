import apsw
from time import time

# TODO parameter placeholders
# TODO explode
# TODO grouping

# NEW
import re
def regexp(expr, item):
	r = re.compile(expr,re.U)
	return r.search(item) is not None

def _map_fun(sql, part, path, combiner, functions, aggregates):
	t0=time()
	db = apsw.Connection(path)
	
	# new
	db.createscalarfunction('regexp',regexp,2)
	
	for x in functions:
		db.createscalarfunction(*x)
	for x in aggregates:
		db.createaggregatefunction(*x)
	
	result = db.cursor().execute(sql)
	try:
		description = result.description
	except:
		description = []
	out = {}
	out['rows'] = list(result)
	out['cols'] = [x[0] for x in description]
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


if __name__=="__main__":
	PARTS = []
	map_sql("drop table if exists test",range(4),lambda x:'data/mr2_{}'.format(x))
	map_sql("create virtual table if not exists test using fts5(a,b)",range(4),lambda x:'data/mr2_{}'.format(x))
