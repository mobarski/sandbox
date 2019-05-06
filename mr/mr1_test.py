from mr1 import *

# ------------------------------------------------------------------------------

if __name__=="xxx__main__":
	import multiprocessing as mp
	pool = mp.Pool(2)

	def get_part_path(part):
		return 'data/{}'.format(part)

	out = map_sql("""
			select x, count(1) as count
			from test
			group by x
		"""
		,[0,1,2,3,4,5,6,7]
		,get_part_path
		#,pool=pool
		)

	for x in reduce_sql("""
				select x, sum(count) as count
				from part group by x
				order by count desc
			""", out
			):
		print(x)


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

#from marshal import dumps,loads
#from json import dumps,loads
from pickle import dumps,loads
from collections import Counter
import re

# v1 -------------------
def tf(map_fun_output):
	out = map_fun_output
	
	tf = Counter()
	for row in out['rows']:
		tokens = re.findall('(?u)\w+',row[0])
		tf.update(tokens)
	if 0:
		out['cols'] = ['grp','tf']
		out['rows'] = [('all',dict(tf))]
	else:
		out['cols'] = ['term','freq']
		out['rows'] = tf.items()
	return out
# -------------

# v2 -----
class TF:
	def __init__(self):
		self.tf = Counter()
	def step(self, value):
		tokens = re.findall('(?u)\w+',value)
		self.tf.update(tokens)
	def finalize(self):
		#return buffer(dumps(dict(self.tf))) # marshal -> pool.map hangs
		return dumps(dict(self.tf)) # pickle -> ok, json -> ok
		
def tf2(map_fun_output):
	out = map_fun_output
	tf = Counter()
	for row in out['rows']:
		tf.update(loads(row[0]))
	out['cols'] = ['term','freq']
	out['rows'] = tf.items()
	return out
# -------------


if __name__=="__main__":
	from pprint import pprint
	import multiprocessing as mp
	pool = mp.Pool(2)
	
	def get_part_path(part):
		return 'data/{}'.format(part)

	for i in range(2):
		if 1: # external python combiner
			t0=time()
			out = map_sql("""
					select lower(text)
					from test
				"""
				,[0,1,2,3,4,5,6,7]
				,get_part_path
				,combiner=tf
				,pool=pool
				)
			for x in reduce_sql("""
						select sum(freq) as freq
						from part
					""", out
					):
				print(x)
			#print(time()-t0, sum([sum(p['rows'][0][1].values()) for p in out]))
			print(time()-t0)

		if 1: # internal python combiner
			t0=time()
			out = map_sql("""
					select tf(lower(text)) as tf
					from test
				"""
				,[0,1,2,3,4,5,6,7]
				,get_part_path
				,aggregates=[('tf',1,TF)]
				,combiner=tf2
				,pool=pool
				)
			for x in reduce_sql("""
						select sum(freq) as freq
						from part
					""", out
					):
				print(x)
			#print(time()-t0, sum([sum(loads(p['rows'][0][0]).values()) for p in out]))
			print(time()-t0)
	
	pool.close()
	pool.join()
