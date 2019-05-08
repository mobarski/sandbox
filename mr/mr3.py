
# TODO parallel union
# TODO parallel reduce
# TODO grouping
# TODO explode

# ------------------------------------------------------------------------------

class MR:
	"""
	"""
	def __init__(self, path_fun, pool=None):
		self.path_fun = path_fun
		self.pool = pool
		self.functions = []
		self.aggregates = []
	
	def map(self, sql, args=[], parts=None, combiner=None):
		assert(parts)
		return _map_sql(sql, args, parts, self.path_fun, pool=self.pool,
		                combiner=combiner,
						functions=self.functions,
						aggregates=self.aggregates)
	
	def map_fun(self, fun, kwargs={}, parts=None):
		assert(parts)
		return _map_function(fun, kwargs, parts, self.path_fun, pool=self.pool)
	
	def union(self, map_output):
		return _union(map_output)
	
	def reduce(self, sql, args, map_output):
		db = self.union(map_output)
		return db.cursor().execute(sql,args)

	def udf(self, name, fun, num_args, deterministic=False):
		self.functions += [(name, fun, num_args, deterministic)]

	def udaf(self, name, factory, num_args):
		self.aggregates += [(name, factory, num_args)]

# ------------------------------------------------------------------------------

import apsw
from time import time

def _map_fun(sql, args, part, path, combiner, functions, aggregates):
	t0=time()
	db = apsw.Connection(path)
		
	for x in functions:
		db.createscalarfunction(*x)
	for x in aggregates:
		db.createaggregatefunction(*x)
	
	result = db.cursor().execute(sql,args)
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


def _map_sql(sql, args, parts, path_fun, pool=None, combiner=None, functions=[], aggregates=[]):
	fun_args = [(sql,args,part,path_fun(part),combiner,functions,aggregates) for part in parts]
	if pool:
		out = pool.map(_map_fun1, fun_args)
	else:
		out = map(_map_fun1, fun_args)
	return out

def _map_function(fun, kwargs, parts, path_fun, pool=None):
	fun_args = [dict(part=part,path=path_fun(part),**kwargs) for part in parts]
	if pool:
		out = pool.map(fun, fun_args)
	else:
		out = map(fun, fun_args)
	return out

def _union(map_output):
	tab = 'part' # TODO rename ???
	filtered_output = [p for p in map_output if p['rows']]
	assert(filtered_output) # TODO
	cols = filtered_output[0]['cols']
	db=apsw.Connection(':memory:')
	db.cursor().execute('create table {}({})'.format(tab, ','.join(cols)))
	for p in filtered_output:
		sql = 'insert into {} values({})'.format(tab, ','.join(['?']*len(cols)))
		db.cursor().executemany(sql,p['rows'])
	return db

# ------------------------------------------------------------------------------

import re
def _regexp(expr, item):
	r = re.compile(expr,re.U|re.I)
	return r.search(item) is not None

# ------------------------------------------------------------------------------

def test_map_fun(kv):
	db = apsw.Connection(kv['path'])
	db.cursor().execute("drop table if exists test")
	db.cursor().execute("create virtual table if not exists test using fts5(a,b)")
	db.cursor().execute("insert into test values (?,?)",['xx aa bb','zz ee rr'])
	
if __name__=="__main__":
	PARTS = [0,1,2,3]
	mr=MR(lambda x:'data/mr3_{}'.format(x))
	mr.map("drop table if exists test",[],PARTS)
	mr.map("create virtual table if not exists test using fts5(a,b)",[],PARTS)
	mr.map("insert into test values (?,?)",['to jest test','a to nie jest'],PARTS)
	data = mr.map("select a,b from test",[],PARTS)
	out = list(mr.reduce('select * from part',[],data))
	print(out)
	mr.map_fun(test_map_fun,{},PARTS)
	print(mr.map("select a,b from test",[],PARTS))
	