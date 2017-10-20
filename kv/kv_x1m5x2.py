# encoding: UTF-8

# KV database built on top of SQLite
# (c) 2017 by mobarski (at) gmail (dot) com
# licence: MIT
# version: x1m4 (x-experimental, p-preview, r-release, m-modification)

# TODO - otwieranie bazy w multiprocessingu -> sqlite3.DatabaseError: database disk image is malformed

# CHANGES:
# x1m5 - limit, tab=1 (tab=0 for metadata)
# x1m4 - multiple tables
# x1m3 - key is not serialized, glob key selection for iterators, class renamed

from __future__ import print_function
import sqlite3
from zlib import compress,decompress
##from pickle import loads,dumps
##from cPickle import loads,dumps
from marshal import loads,dumps


class KV:
	"Key-Value database built on top of SQLite"
	def __init__(self,path=':memory:',zlevel=0,protocol=2,tab=1):
		self.tab = 'kv'+str(abs(int(tab)))
		self.path = path
		self.zlevel = zlevel
		self.protocol = protocol
		self.conn = sqlite3.connect(path)
		self.create()
	### SERDE ##
	def ser(self,x):
		if self.zlevel:
			return buffer(compress(dumps(x,self.protocol),self.zlevel))
		else:
			return buffer(dumps(x,self.protocol))
	def de(self,x):
		if self.zlevel:
			return loads(decompress(x))
		else:
			return loads(str(x))
	### CORE ###
	def get(self,key,default=None):
		results = self.conn.execute('select v from {0} where k=?'.format(self.tab),(key,))
		x = results.fetchone()
		return self.de(x[0]) if x else default
	def set(self,key,v):
		val = self.ser(v)
		self.conn.execute('insert or replace into {0} values (?,?)'.format(self.tab),(key, val))
	def incr(self,key,val=1): # XXX
		self.conn.execute('update {0} set v = v + ? where k=?'.format(self.tab),(val,key))
	### ITER ###
	def keys(self,like=None,limit=-1):
		limit_str = "limit "+str(int(limit))
		if like:
			for k in self.conn.execute('select k from {0} where k glob ? {1}'.format(self.tab, limit_str),(like,)):
				yield k[0]
		else:
			for k in self.conn.execute('select k from {0} {1}'.format(self.tab, limit_str)):
				yield k[0]
	def values(self,like=None,limit=-1):
		limit_str = "limit "+str(int(limit))
		if like:
			for v in self.conn.execute('select v from {0} where k glob ? {1}'.format(self.tab, limit_str),(like,)):
				yield self.de(v[0])
		else:
			for v in self.conn.execute('select v from {0} {1}'.format(self.tab, limit_str)):
				yield self.de(v[0])
	def items(self,like=None,limit=-1):
		limit_str = "limit "+str(int(limit))
		if like:
			for k,v in self.conn.execute('select k,v from {0} where k glob ? {1}'.format(self.tab, limit_str),(like,)):
				yield k,self.de(v)			
		else:
			for k,v in self.conn.execute('select k,v from {0} {1}'.format(self.tab, limit_str)):
				yield k,self.de(v)
	def count(self,like=None):
		if like:
			for x in self.conn.execute('select count(1) from {0} where k glob ?'.format(self.tab),(like,)):
				return x[0]
		else:
			for x in self.conn.execute('select count(1) from {0}'.format(self.tab)):
				return x[0]
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
	def remove(self,keys):
		[self.delete(k) for k in keys]
	def size_iter(self,like=None,limit=-1): # TODO rename?
		if like:
			for k,vs in self.conn.execute('select k,length(v) from {0} where k glob ? order by length(v) desc limit ?'.format(self.tab),(like,limit)):
				yield k,vs
		else:
			for k,vs in self.conn.execute('select k,length(v) from {0} order by length(v) desc limit ?'.format(self.tab),(limit,)):
				yield k,vs
	### OTHER ###
	def tables(self):
		rows = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
		return [int(r[0][2:]) for r in rows]
	def commit(self):
		self.conn.commit()
	def create(self):
		self.conn.execute('create table if not exists {0} (k,v)'.format(self.tab))
		self.conn.execute('create unique index if not exists i_{0} on {0} (k)'.format(self.tab))
	def delete(self,key):
		self.conn.execute('delete from {0} where k=?'.format(self.tab),(key,))
	def clear(self):
		self.conn.execute('drop table {0}'.format(self.tab))
		self.create()
		self.vacuum()
	def vacuum(self):
		self.conn.execute('vacuum')
	def size(self,key):
		results = self.conn.execute('select length(v) from {0} where k=?'.format(self.tab),(key,))
		x = results.fetchone()
		return x[0] if x else None
	### DICT ###
	def __getitem__(self,k): return self.get(k)
	def __setitem__(self,k,v): return self.set(k,v)
	def __contains__(self,k): return self.size(k) is not None
	def __delitem__(self,k): return self.delete(k)
	### ### ###

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
	db = KV('bench_x1m5.db',0)
	#db = KV()
	data = {'k'+str(i):'v'+str(i) for i in range(N)}
	#data = {i:'v'+str(i) for i in range(N)}
	if mode=='write':
		db.clear()
		db.commit()
		t0=time()
		db.update(data.items())
		t1=time()
		db.commit()
		t2=time()
		print('WRITE rows/s',int(N/(t2-t0)), "total {0:.2f}s".format(t2-t0), "update {0:.2f}s".format(t1-t0), "commit {0:.2f}s".format(t2-t1))
		db.remove(db.keys())
	if mode=='incr':
		t0=time()
		for k in data:
			db.incr(k,1.1)
		t1=time()
		db.commit()
		t2=time()
		print('INCR rows/s',int(N/(t2-t0)), "total {0:.2f}s".format(t2-t0), "update {0:.2f}s".format(t1-t0), "commit {0:.2f}s".format(t2-t1))
	if mode=='read':
		t0=time()
		[db.get(k) for k in data]
		t1=time()
		print('READ rows/s',int(N/(t1-t0)), "total {0:.2f}s".format(t1-t0))
	if mode=='keys':
		t0=time()
		[k for k in db.keys()][:10]
		t1=time()
		print('KEYS rows/s',int(N/(t1-t0)), "total {0:.2f}s".format(t1-t0))

if __name__=="__main__":
	for i in range(10): bench_kv(100000,'incr')
	#test_kv()
