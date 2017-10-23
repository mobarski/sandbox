# encoding: UTF-8

# KEY-COLUMN-VALUE database built on top of SQLite
# (c) 2017 by mobarski (at) gmail (dot) com
# licence: MIT
# version: (x-experimental, p-preview, r-release, m-modification)

from __future__ import print_function
import sqlite3
from itertools import groupby

class KCV:
	def __init__(self, path=':memory:', tab='main'):
		self.path = path
		self.tab = tab # TODO sanitize?
		self.conn = sqlite3.connect(path)
		self.create()
	def create(self):
		self.conn.execute('create table if not exists {0} (k,c,v)'.format(self.tab))
		self.conn.execute('create unique index if not exists i_{0} on {0} (k,c)'.format(self.tab))
	### CORE - WRITE ###
	def set(self,k,c,v):
		self.conn.execute('insert or replace into {0} values (?,?,?)'.format(self.tab),(k,c,v))
	def store(self,k,items):
		self.conn.executemany('insert or replace into {0} values (?,?,?)'.format(self.tab),((k,c,v) for c,v in items))
	def incr(self,k,c,v=1):
		self.conn.execute('insert or replace into {0} values (?,?,?+coalesce((select v from {0} where k=? and c=?),0))'.format(self.tab),(k,c,v,k,c))
	# TODO incr many
	### CORE - READ ###
	def get(self,k,c,default=None):
		x = self.conn.execute('select v from {0} where k=? and c=?'.format(self.tab),(k,c)).fetchone()
		return x[0] if x else default
	def items(self,k):
		return dict(self.iteritems(k))
	def scan(self,k='*',c='*',order=''):
		it = self.iterscan(k=k,c=c,order=order)
		for k,g in groupby(it,key=lambda x:x[0]):
			yield k,[(x[1],x[2]) for x in g]
	def iterscan(self,k='*',c='*',order=''):
		order_str = self.get_order_str(order)
		# TODO limit?
		# TODO noglob
		# TODO from_c to_c
		# TODO from_k to_k
		for k,c,v in self.conn.execute('select k,c,v from {0} where k glob ? and c glob ? {1}'.format(self.tab,order_str),(k,c)):
			yield k,c,v
	def iteritems(self,k):
		for c,v in self.conn.execute('select c,v from {0} where k=?'.format(self.tab),(k,)):
			yield c,v
	### SQL CODE GENERATION UTILS ###
	def get_order_str(self,order):
		out = []
		if 'ka' in order: out += ['k asc']
		if 'kd' in order: out += ['k desc']
		if 'va' in order: out += ['v asc']
		if 'vd' in order: out += ['v desc']
		if 'ca' in order: out += ['c asc']
		if 'cd' in order: out += ['c desc']
		if out: return 'order by '+','.join(out)
		else: return ''

db = KCV()
db.store('u1',dict(name='maciej',eyes='blue',nick='kerbal').items())
db.store('u2',dict(name='agnieszka',eyes='green',nick='felia').items())
db.store('u3',dict(name='mikolaj',eyes='blue',nick='miki').items())
db.store('u4',dict(name='jan',eyes='blue',nick='roszek').items())
print(db.items('u1'))
print(list(db.iterscan(order='')))
db.incr('kx','cx',30)
db.incr('kx','cx',10)
db.incr('kx','cx',2.5)
print(db.get('kx','cx'))
