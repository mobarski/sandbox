# encoding: UTF-8

## KV databases family built on top of SQLite
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: x1m2 (x-experimental, p-preview, r-release, m-modification)

from __future__ import print_function
import sqlite3
from zlib import compress,decompress
#from pickle import loads,dumps
#from cPickle import loads,dumps
from marshal import loads,dumps

# TODO:
# [ ] separate ser+de for key, benchmark

class blob_kv:
	"Key-Value database built on top of SQLite"
	def __init__(self,path=':memory:',zlevel=0,protocol=2):
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
	def get(self,k,default=None):
		key=self.ser(k)
		results = self.conn.execute('select v from kv where k=?',(key,))
		x = results.fetchone()
		return self.de(x[0]) if x else default
	def set(self,k,v):
		key=self.ser(k)
		val = self.ser(v)
		self.conn.execute('insert or replace into kv values (?,?)',(key,val))
	### ITER ###
	def keys(self):
		for k in self.conn.execute('select k from kv'):
			yield self.de(k[0])
	def values(self):
		for v in self.conn.execute('select v from kv'):
			yield self.de(v[0])
	def items(self):
		for k,v in self.conn.execute('select k,v from kv'):
			yield self.de(k),self.de(v)
	def count(self):
		for x in self.conn.execute('select count(1) from kv'):
			return x[0]
	def update(self,items):
		ser = self.ser
		self.conn.executemany('insert or replace into kv values (?,?)',[(ser(k),ser(v)) for k,v in items]) # best-of-5:205k/s
		##from itertools import starmap
		##ser2 = lambda x:(ser(x[0]),ser(x[1]))
		##ser3 = lambda k,v:(ser(k),ser(v))
		##self.conn.executemany('insert or replace into kv values (?,?)',starmap(ser3,items)) # best-of-5:192k/s
		##self.conn.executemany('insert or replace into kv values (?,?)',((ser(k),ser(v)) for k,v in items)) # best-of-5:191k/s
		##self.conn.executemany('insert or replace into kv values (?,?)',map(ser2,items)) # best-of-5:188k/s
		##self.conn.executemany('insert or replace into kv values (?,?)',[map(ser,kv) for kv in items]) # best-of-5:168k/s
		##[self.set(k,v) for k,v in items] # best-of-5:144k/s
	def size_iter(self,limit=-1): # TODO rename?
		for k,vs in self.conn.execute('select k,length(v) from kv order by length(v) desc limit ?',(limit,)):
			yield self.de(k),vs
	### OTHER ###
	def commit(self):
		self.conn.commit()
	def create(self):
		self.conn.execute('create table if not exists kv (k blob,v blob)')
		self.conn.execute('create unique index if not exists i_kv on kv (k)')		
	def delete(self,k):
		key=self.ser(k)
		self.conn.execute('delete from kv where k=?',(key,))
	def truncate(self):
		self.conn.execute('drop table kv')
		self.create()
		self.vacuum()
	def vacuum(self):
		self.conn.execute('vacuum')
	def size(self,k):
		key=self.ser(k)
		results = self.conn.execute('select length(v) from kv where k=?',(key,))
		x = results.fetchone()
		return x[0] if x else None
	### DICT ###
	def __getitem__(self,k): return self.get(k)
	def __setitem__(self,k,v): return self.set(k,v)
	def __contains__(self,k): return self.size(k) is not None
	def __delitem__(self,k): return self.delete(k)
	### ### ###

def test_kv():
	db = blob_kv('usunmnie.db')
	#db.set('a','to jest test żółć')
	db.set('a','to jest test')
	#db.set('b',['to','jest','test','żółć'])
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
	db.truncate()
	print(db.count())
	db.commit()
	db['x'] = 42
	print(db['x'])
	print('x' in db)
	del db['x']

def bench_kv(N,mode='write'):
	from time import time
	#db = blob_kv('bench.db',0)
	db = blob_kv()
	data = {'k'+str(i):'v'+str(i) for i in range(N)}
	if mode=='write':
		db.truncate()
		db.commit()
		t0=time()
		db.update(data.items())
		t1=time()
		db.commit()
		t2=time()
		print('WRITE rows/s',int(N/(t2-t0)), "total {0:.2f}s".format(t2-t0), "update {0:.2f}s".format(t1-t0), "commit {0:.2f}s".format(t2-t1))
	if mode=='read':
		t0=time()
		[db.get(k) for k in data]
		t1=time()
		print('READ rows/s',int(N/(t1-t0)), "total {0:.2f}s".format(t1-t0))
	

if __name__=="__main__":
	for i in range(10):
		bench_kv(100000,'write')
	#test_kv()
