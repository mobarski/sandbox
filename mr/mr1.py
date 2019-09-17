import sqlite3
import apsw
from time import time

USE_APSW = False

# TODO explode
# TODO grouping
# TODO parameter placeholders

# XXX REFACTOR XXX
import re
rem_at_re = re.compile('@[\w.-]+',re.U)
def _regexp(expr, item):
	r = re.compile(expr,re.U|re.I)
	if '@' not in expr: # XXX
		item = rem_at_re.sub(' ',item) # XXX
	match = r.search(item)
	return match is not None

def _snip(expr, left, right, item):
	if not item: return ''
	r = re.compile(ur'(?u)\b[\w\s]{{0,{}}}(?:{})[\w\s]{{0,{}}}\b'.format(left,expr,right),re.U)
	match = r.search(item)
	return match.group() if match else ''

def _execute(sql, args, path, fun_list, agg_list):

	if USE_APSW:
		db = apsw.Connection(path)
		# functions
		db.createscalarfunction('regexp',_regexp,2)
		for x in fun_list:
			pass # TODO
		for x in agg_list:
			pass # TODO
	else:
		db = sqlite3.connect(path)
		# functions
		db.create_function('regexp',2,_regexp)
		db.create_function('snip',4,_snip)
		for x in fun_list:
			db.create_function(*x)
		for x in agg_list:
			db.create_aggregate(*x)
	
	return db.cursor().execute(sql,args)

def _map_fun(sql, args, part, path, combiner, fun_list, agg_list):
	t0=time()

	result = _execute(sql, args, path, fun_list, agg_list)
	
	out = {}
	out['cols'] = [x[0] for x in result.description] # APSW ERROR: ExecutionCompleteError: Can't get description for statements that have completed execution
	out['rows'] = list(result)
	out['part'] = part
	out['map_time'] = time()-t0
	if combiner:
		t0=time()
		out = combiner(out)
		out['combine_time'] = time()-t0
	return out


def _map_fun1(args):
	return _map_fun(*args)


# --- API ----------------------------------------------------------------------

def map_sql(sql, parts, path_fun, args=[], pool=None, combiner=None, fun_list=[], agg_list=[]):
	_args = [(sql,args,part,path_fun(part),combiner,fun_list,agg_list) for part in parts]
	if pool:
		out = pool.map(_map_fun1, _args)
	else:
		out = map(_map_fun1, _args)
	return out

def iter_sql(sql, args, parts, path_fun, fun_list=[], agg_list=[]):
	for part in parts:
		path = path_fun(part)
		for row in _execute(sql, args, path, fun_list, agg_list):
			yield row

def union(map_output):
	db=sqlite3.connect(':memory:')
	tab = 'part' # TODO rename ???
	filtered_output = [p for p in map_output if p['rows']]
	#print('filtered_len',[len(x['rows']) for x in filtered_output]) # XXX
	#print('filtered_cols',[x['cols'] for x in filtered_output]) # XXX
	if not filtered_output:
		return db
	cols = filtered_output[0]['cols']
	db.cursor().execute('create table {}({})'.format(tab, ','.join(cols)))
	for p in filtered_output:
		sql = 'insert into {} values({})'.format(tab, ','.join(['?']*len(cols)))
		db.cursor().executemany(sql,p['rows'])
	return db
