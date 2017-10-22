# encoding: UTF-8

# KV database built on top of SQLite
# (c) 2017 by mobarski (at) gmail (dot) com
# licence: MIT
# version: x7 (x-experimental, p-preview, r-release, m-modification)

# TODO - multiprocessing fix -> sqlite3.DatabaseError: database disk image is malformed
# TODO - RENAME kv is already taken on pypi -> kv2? xkv
# TODO - lock/pipe/atomic

# CHANGES:
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
			self.ser = lambda x: buffer(dumps(x,protocol))
			self.de  = lambda x: loads(str(x))
		else:
			self.ser = lambda x:x
			self.de  = lambda x:x
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
	### ANALYTICS AND AGGREGATIONS ###
	def incr(self,key,val=1):
		self.conn.execute('update {0} set v=v+? where k=?'.format(self.tab),(val,key))
	def sum(self,pattern=None):
		if pattern:
			for x in self.conn.execute('select sum(v) from {0} where k glob ?'.format(self.tab),(pattern,)):
				return x[0]
		else:
			for x in self.conn.execute('select sum(v) from {0}'.format(self.tab)):
				return x[0]
	def min(self,pattern=None):
		if pattern:
			for x in self.conn.execute('select min(v) from {0} where k glob ?'.format(self.tab),(pattern,)):
				return x[0]
		else:
			for x in self.conn.execute('select min(v) from {0}'.format(self.tab)):
				return x[0]
	def max(self,pattern=None):
		if pattern:
			for x in self.conn.execute('select max(v) from {0} where k glob ?'.format(self.tab),(pattern,)):
				return x[0]
		else:
			for x in self.conn.execute('select max(v) from {0}'.format(self.tab)):
				return x[0]
	def count(self,pattern=None):
		if pattern:
			for x in self.conn.execute('select count(1) from {0} where k glob ?'.format(self.tab),(pattern,)):
				return x[0]
		else:
			for x in self.conn.execute('select count(1) from {0}'.format(self.tab)):
				return x[0]				
	### ITER ###
	def keys(self,pattern=None,limit=-1,order=''):
		limit_str = self.get_limit_str(limit)
		order_str = self.get_order_str(order)
		if pattern:
			for k in self.conn.execute('select k from {0} where k glob ? {1} {2}'.format(self.tab, order_str, limit_str),(pattern,)):
				yield k[0]
		else:
			for k in self.conn.execute('select k from {0} {1} {2}'.format(self.tab, order_str, limit_str)):
				yield k[0]
	def values(self,pattern=None,limit=-1,order=''):
		limit_str = self.get_limit_str(limit)
		order_str = self.get_order_str(order)
		if pattern:
			for v in self.conn.execute('select v from {0} where k glob ? {1} {2}'.format(self.tab, order_str, limit_str),(pattern,)):
				yield self.de(v[0])
		else:
			for v in self.conn.execute('select v from {0} {1} {2}'.format(self.tab, order_str, limit_str)):
				yield self.de(v[0])
	def items(self,pattern=None,limit=-1,order=''):
		limit_str = self.get_limit_str(limit)
		order_str = self.get_order_str(order)
		if pattern:
			for k,v in self.conn.execute('select k,v from {0} where k glob ? {1} {2}'.format(self.tab, order_str, limit_str),(pattern,)):
				yield k,self.de(v)			
		else:
			for k,v in self.conn.execute('select k,v from {0} {1} {2}'.format(self.tab, order_str, limit_str)):
				yield k,self.de(v)
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
	##
	def remove(self,keys):
		[self.delete(k) for k in keys]

	def compact(self): # TODO rename?
		self.conn.execute('vacuum')
	##
	def size(self,key):
		results = self.conn.execute('select length(v) from {0} where k=?'.format(self.tab),(key,))
		x = results.fetchone()
		return x[0] if x else None
	def size_iter(self,pattern=None,limit=-1): # TODO rename?
		if pattern:
			for k,vs in self.conn.execute('select k,length(v) from {0} where k glob ? order by length(v) desc limit ?'.format(self.tab),(pattern,limit)):
				yield k,vs
		else:
			for k,vs in self.conn.execute('select k,length(v) from {0} order by length(v) desc limit ?'.format(self.tab),(limit,)):
				yield k,vs

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
		pass # TODO
	# TODO def pop(
	# TODO def popitem(
	# TODO def setdefault(
	### UTIL ###
	def get_limit_str(self, limit):
		return "limit "+str(int(limit))
	def get_order_str(self, order):
		if order=='ka': return 'order by k asc'
		elif order=='kd': return 'order by k desc'
		elif order=='va': return 'order by v asc'
		elif order=='vd': return 'order by v desc'
		else: return ''

def test_kv():
	db = KV('usunmnie.db')
	##db.set('a','to jest test żółć')
	db.set('a','to jest test')
	##db.set('b',['to','jest','test','żółć'])
	db.set('b',['to','jest','test'])
	db.set('c',{'to':1,'jest':2,'test':3})
	db.commit()
	for k,v in db.items():
		print(k,v)
	for k,lv in db.size_iter():
		v = db.get(k)
		print(k,lv,v)
	print(db.size('a'))
	print(list(db.keys()))
	print(db.count())
	db.delete('a')
	print(db.count())
	db.clear()
	print(db.count())
	db.commit()
	db['x'] = 42
	print(db['x'])
	print('x' in db)
	del db['x']
	print(db.tables())


def bench_kv(N,mode='write'):
	from time import time
	db = KV('bench_x7.db',-1)
	#db = KV()
	#data = {'k'+str(i):str(i)+'.0' for i in range(N)}
	data = {'k'+str(i):i for i in range(N)}
	#data = {i:'v'+str(i) for i in range(N)}
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
	#print(list(db.items(limit=3)))
	print(list(db.items(limit=10,order='va')))
	print(db.sum())
	print(db.min())
	print(db.max())
	print(db.tables())

if __name__=="__main__":
	#for i in range(10): bench_kv(100000,'write')
	for i in range(10): bench_kv(100000,'write')
	for i in range(10): bench_kv(100000,'keys')
	#test_kv()
