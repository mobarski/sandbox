
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
		self.functions = [('regexp',2,_regexp)]
		self.aggregates = []
	
	def map(self, sql, args=[], parts=None, combiner=None):
		assert(parts)
		print(sql)
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

	def udf(self, name, num_args, fun):
		self.functions += [(name, num_args, fun)]

	def udaf(self, name, num_args, factory):
		self.aggregates += [(name, num_args, factory)]

# ------------------------------------------------------------------------------

import sqlite3
from time import time

def _map_fun(sql, args, part, path, combiner, functions, aggregates):
	t0=time()
	db = sqlite3.connect(path)
		
	for x in functions:
		db.create_function(*x)
	for x in aggregates:
		db.create_aggregate(*x)
	
	result = db.execute(sql,args)
	db.commit()
	out = {}
	out['rows'] = list(result)
	out['cols'] = [x[0] for x in result.description or []]
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
	db=sqlite3.connect(':memory:')
	db.execute('create table {}({})'.format(tab, ','.join(cols)))
	for p in filtered_output:
		sql = 'insert into {} values({})'.format(tab, ','.join(['?']*len(cols)))
		db.executemany(sql,p['rows'])
	return db

# ------------------------------------------------------------------------------

import re
def _regexp(expr, item):
	r = re.compile(expr,re.U|re.I)
	return r.search(item) is not None

# ------------------------------------------------------------------------------

def test_map_fun(kv):
	db = sqlite3.connect(kv['path'])
	db.execute("drop table if exists test")
	db.execute("create virtual table if not exists test using fts4(a,b)")
	db.execute("insert into test values (?,?)",['xx aa bb','zz ee rr'])
	
if __name__=="__main__":
	PARTS = [0,1,2,3]
	mr=MR(lambda x:'data/mr4_{}'.format(x))
	mr.map("drop table if exists test",[],PARTS)
	#mr.map("create table if not exists test(a,b)",[],PARTS)
	mr.map("create virtual table if not exists test using fts4(a,b)",[],PARTS)
	mr.map("insert into test values (?,?)",['to jest test','a to nie jest'],PARTS)
	data = mr.map("select a,b from test",[],PARTS)
	print(data)
	out = list(mr.reduce('select * from part',[],data))
	print(out)
	mr.map_fun(test_map_fun,{},PARTS)
	print(mr.map("select a,b from test",[],PARTS))
	