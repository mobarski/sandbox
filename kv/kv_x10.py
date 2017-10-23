# encoding: UTF-8

# KV database built on top of SQLite
# (c) 2017 by mobarski (at) gmail (dot) com
# licence: MIT
# version: x10 (x-experimental, p-preview, r-release, m-modification)

# TODO - multiprocessing fix -> sqlite3.DatabaseError: database disk image is malformed
# TODO - RENAME kv is already taken on pypi -> kv2? xkv
# TODO - lock/pipe/atomic/batch

# CHANGES:
# x10 - agg:min,max,sum,count  scan:klen  sync on __exit__
# x9 - scan=range, keys/values/items as scan call, vk mode
# x8 - range
# x7 - init_serde,__enter__,__exit__,__iter__,has_key,close
# x1m6 - -1=no_serde, commit->sync, incr, order, sum, min, max, tab as str
# x1m5 - limit, tab=1 (tab=0 for metadata)
# x1m4 - multiple tables
# x1m3 - key is not serialized, glob key selection for iterators, class renamed

from __future__ import print_function
import sqlite3
from zlib import compress,decompress
from marshal import loads,dumps


class KV:
	"Key-Value database built on top of SQLite"
	def __init__(self, path=':memory:', zlevel=0, indexed=0, tab='main'):
		self.path = path
		self.tab = tab # TODO sanitize?
		self.conn = sqlite3.connect(path)
		self.create()
		self.indexed(indexed)
		self.init_serde(zlevel)
	def init_serde(self,zlevel):
		protocol = 2
		if zlevel>0:
			self.ser = lambda x: buffer(compress(dumps(x,protocol),zlevel))
			self.de  = lambda x: loads(decompress(x))
		elif zlevel==0:
			#self.ser = lambda x: buffer(dumps(x,protocol))
			#self.de  = lambda x: loads(str(x))
			self.ser = lambda x: dumps(x,protocol)
			self.de  = lambda x: loads(str(x))
		else:
			self.ser = lambda x:x
			self.de  = lambda x:x
	def execute(self,sql,vals):
		#print('EXECUTE',sql,vals)
		return self.conn.execute(sql,vals)
	### CORE ###
	def get(self,key,default=None):
		results = self.conn.execute('select v from {0} where k=?'.format(self.tab),(key,))
		x = results.fetchone()
		return self.de(x[0]) if x else default
	def set(self,key,v):
		val = self.ser(v)
		self.conn.execute('insert or replace into {0} values (?,?)'.format(self.tab),(key, val))
	def delete(self,key):
		self.conn.execute('delete from {0} where k=?'.format(self.tab),(key,))			
	### ITER ###
	def keys(self, like=None, limit=-1, order=''):
		for k in self.scan(mode='k', like=like,limit=limit,order=order):
			yield k
	def values(self, like=None, limit=-1, order=''):
		for v in self.scan(mode='v', like=like,limit=limit,order=order):
			yield v
	def items(self, like=None, limit=-1, order=''):
		for k,v in self.scan(mode='kv', like=like,limit=limit,order=order):
			yield k,v			
	def scan(self, mode='k', like=None, limit=-1, order='', from_k=None, to_k=None, from_eq=True, to_eq=True): # TODO args order
		where_str,vals = self.get_where_str_vals(from_k,to_k,from_eq,to_eq,like)
		limit_str = self.get_limit_str(limit)
		order_str = self.get_order_str(order)
		if mode=='k':
			for [k] in self.execute('select k from {0} {1} {2} {3}'.format(self.tab, where_str, order_str, limit_str),vals):
				yield k
		elif mode=='kv':
			for k,v in self.execute('select k,v from {0} {1} {2} {3}'.format(self.tab, where_str, order_str, limit_str),vals):
				yield k, self.de(v)
		elif mode=='vk':
			for k,v in self.execute('select k,v from {0} {1} {2} {3}'.format(self.tab, where_str, order_str, limit_str),vals):
				yield self.de(v), k
		elif mode=='v':
			for [v] in self.execute('select v from {0} {1} {2} {3}'.format(self.tab, where_str, order_str, limit_str),vals):
				yield self.de(v)
		elif mode=='klen':
			for k,v in self.execute('select k,length(v) from {0} {1} {2} {3}'.format(self.tab, where_str, order_str, limit_str),vals):
				yield k,v
	def agg(self, mode='sum', like=None, limit=-1, order='', from_k=None, to_k=None, from_eq=True, to_eq=True): # TODO args order
		where_str,vals = self.get_where_str_vals(from_k,to_k,from_eq,to_eq,like)
		limit_str = self.get_limit_str(limit)
		order_str = self.get_order_str(order)
		if mode=='sum':
			for [x] in self.execute('select sum(v) from {0} {1} {2} {3}'.format(self.tab, where_str, order_str, limit_str),vals):
				return x
		elif mode=='count':
			for [x] in self.execute('select count(1) from {0} {1} {2} {3}'.format(self.tab, where_str, order_str, limit_str),vals):
				return x
		elif mode=='min':
			for [x] in self.execute('select min(v) from {0} {1} {2} {3}'.format(self.tab, where_str, order_str, limit_str),vals):
				return x
		elif mode=='max':
			for [x] in self.execute('select max(v) from {0} {1} {2} {3}'.format(self.tab, where_str, order_str, limit_str),vals):
				return x
	### DICT AND SHELVE INTERFACE ###
	def __getitem__(self,k): return self.get(k)
	def __setitem__(self,k,v): return self.set(k,v)
	def __delitem__(self,k): return self.delete(k)
	def __contains__(self,k): return self.size(k) is not None
	def __iter__(self): return self.keys()
	def __len__(self): return self.count()
	def has_key(self,k): return self.size(k) is not None
	def clear(self):
		self.conn.execute('drop table {0}'.format(self.tab))
		self.create()
		self.compact()
	def update(self,items):
		ser = self.ser
		self.conn.executemany('insert or replace into {0} values (?,?)'.format(self.tab),[(k,ser(v)) for k,v in items]) # best-of-5:205k/s
		##from itertools import starmap
		##ser2 = lambda x:(ser(x[0]),ser(x[1]))
		##ser3 = lambda k,v:(ser(k),ser(v))
		##self.conn.executemany('insert or replace into kv values (?,?)',starmap(ser3,items)) # best-of-5:192k/s
		##self.conn.executemany('insert or replace into kv values (?,?)',((ser(k),ser(v)) for k,v in items)) # best-of-5:191k/s
		##self.conn.executemany('insert or replace into kv values (?,?)',map(ser2,items)) # best-of-5:188k/s
		##self.conn.executemany('insert or replace into kv values (?,?)',[map(ser,kv) for kv in items]) # best-of-5:168k/s
		##[self.set(k,v) for k,v in items] # best-of-5:144k/s
	def sync(self):
		self.conn.commit()
	def close(self):
		self.conn.commit()
	def __enter__(self):
		return self
	def __exit__(self, ex_type, ex_val, ex_tb):
		if ex_type is None:
			self.sync()
		else:
			print('EXIT',ex_type,ex_val,ex_tb) # TODO
	# TODO def pop(
	# TODO def popitem(
	# TODO def setdefault(
	### OTHER ###
	def create(self):
		self.conn.execute('create table if not exists {0} (k,v)'.format(self.tab))
		self.conn.execute('create unique index if not exists i_{0} on {0} (k)'.format(self.tab))
	def indexed(self, is_indexed=False):
		if is_indexed:
			self.conn.execute('create index if not exists iv_{0} on {0} (v)'.format(self.tab))
		else:
			self.conn.execute('drop index if exists iv_{0}'.format(self.tab))
	def tables(self):
		rows = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
		return [r[0] for r in rows]
	def remove(self,keys):
		[self.delete(k) for k in keys]

	def compact(self): # TODO rename?
		self.conn.execute('vacuum')
	def size(self,key):
		results = self.conn.execute('select length(v) from {0} where k=?'.format(self.tab),(key,))
		x = results.fetchone()
		return x[0] if x else None
	def incr(self,key,val=1):
		self.conn.execute('update {0} set v=v+? where k=?'.format(self.tab),(val,key))
	# TODO def copyto(
	### ANALYTICS AND AGGREGATIONS ###
	def count(self,like=None):
		return self.agg(mode='count', like=like)
	def sum(self,like=None):
		return self.agg(mode='sum', like=like)
	def min(self,like=None):
		return self.agg(mode='min', like=like)
	def max(self,like=None):
		return self.agg(mode='max', like=like)
	# TODO UDF
	# TODO UDAF
	### SQL CODE GEN UTILS ###
	def get_limit_str(self, limit):
		return "limit "+str(int(limit))
	def get_order_str(self, order):
		if order=='ka': return 'order by k asc'
		elif order=='kd': return 'order by k desc'
		elif order=='va': return 'order by v asc'
		elif order=='vd': return 'order by v desc'
		else: return ''
	def get_where_str_vals(self,from_k,to_k,from_eq,to_eq,like):
		if from_k is None and to_k is None and like is None: return u'',[]
		sql = ['where']
		vals = []
		if from_k != None:
			sql.extend(['k','>=' if from_eq else '>','?'])
			vals.append(from_k)
		if from_k != None and to_k != None: sql.append('and')
		if to_k != None:
			sql.extend(['k','<=' if to_eq else '<','?'])
			vals.append(to_k)
		if to_k != None and like != None: sql.append('and')
		if like != None:
			sql.extend(['k','glob','?'])
			vals.append(like)
		return u' '.join(sql),vals

def test_kv():
	db = KV('usunmnie.db',0)
	##db.set('a','to jest test żółć')
	db.set('a','to jest test')
	##db.set('b',['to','jest','test','żółć'])
	db.set('b',['to','jest','test'])
	db.set('c',{'to':1,'jest':2,'test':3})
	db.sync()
	print('ITEMS')
	for k,v in db.items():
		print(k,v)
	print('KEYS')
	for k in db.keys():
		print(k)

	print('KLEN')
	for k,lv in db.scan('klen'):
		v = db.get(k)
		print(k,lv,v)
	print(db.size('a'))
	print(list(db.keys()))
	print(db.count())
	db.delete('a')
	print(db.count())
	db.clear()
	print(db.count())
	db.sync()
	with KV('usunmnie.db',0) as db:
		db['x'] = 42
		print(db['x'])
		print('x' in db)
		del db['x']
		print(db.tables())


def bench_kv(N,mode='write'):
	from time import time
	db = KV('bench_x10.db',-1)
	#db = KV()
	#data = {'k'+str(i):str(i)+'.0' for i in range(N)}
	#data = {'k'+str(i):i for i in range(N)}
	data = {i:i for i in range(N)}
	if mode=='write':
		db.clear()
		db.sync()
		t0=time()
		db.update(data.items())
		t1=time()
		db.sync()
		t2=time()
		print('WRITE rows/s',int(N/(t2-t0)), "total {0:.2f}s".format(t2-t0), "update {0:.2f}s".format(t1-t0), "commit {0:.2f}s".format(t2-t1))
	if mode=='incr':
		t0=time()
		[db.incr(k) for k in data]
		t1=time()
		print('INCR rows/s',int(N/(t1-t0)), "total {0:.2f}s".format(t1-t0))
	if mode=='read':
		t0=time()
		[db.get(k) for k in data]
		t1=time()
		print('READ rows/s',int(N/(t1-t0)), "total {0:.2f}s".format(t1-t0))
	if mode=='keys':
		t0=time()
		[k for k in db.keys(order='vd')]
		t1=time()
		print('KEYS rows/s',int(N/(t1-t0)), "total {0:.2f}s".format(t1-t0))
	if mode=='scan':
		t0=time()
		out=[k for k in db.scan(1,20,1,1,order='ka')]
		t1=time()
		print('SCAN rows/s',int(N/(t1-t0)), "total {0:.2f}s".format(t1-t0),len(out),list(out)[:10])
	#print(list(db.items(limit=3)))
	## print(list(db.items(limit=10,order='va')))
	## print(db.sum())
	## print(db.min())
	## print(db.max())
	## print(db.tables())

if __name__=="__main__":
	#for i in range(1): bench_kv(100000,'write')
	#for i in range(1): bench_kv(100000,'scan')
	#for i in range(10): bench_kv(100000,'keys')
	test_kv()
	