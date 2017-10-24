# encoding: UTF-8

# KEY-COLUMN-VALUE database built on top of SQLite
# (c) 2017 by mobarski (at) gmail (dot) com
# licence: MIT
# version: x1m2 (x-experimental, p-preview, r-release, m-modification)

# x1m2 - incr_many,benchmark,limit,delete,sync,to_col_store(x2),from_col_store(x2)

from __future__ import print_function
import sqlite3
from itertools import groupby

class KCV:
	def __init__(self, path=':memory:', tab='main'):
		self.path = path
		self.tab = tab # TODO sanitize?
		self.conn = sqlite3.connect(path)
		self.create()
	def create(self,index=True):
		self.conn.execute('create table if not exists {0} (k,c,v)'.format(self.tab))
		if index:
			self.conn.execute('create unique index if not exists i_{0} on {0} (k,c)'.format(self.tab))
	def execute(self,*a,**kw):
		print('EXECUTE',*a,**kw)
		return self.conn.execute(*a,**kw)
	### CORE - WRITE ###
	def sync(self,compact=False):
		if compact:
			self.conn.execute('vacuum')
		self.conn.commit()
	def set(self,k,c,v):
		self.conn.execute('insert or replace into {0} values (?,?,?)'.format(self.tab),(k,c,v))
	def store(self,k,items):
		self.conn.executemany('insert or replace into {0} values (?,?,?)'.format(self.tab),((k,c,v) for c,v in items))
	def incr(self,k,c,v=1):
		self.conn.execute('insert or replace into {0} values (?,?,?+coalesce((select v from {0} where k=? and c=?),0))'.format(self.tab),(k,c,v,k,c))
	def incr_many(self,k,items): # TODO rename: add? incriter incr_items
		self.conn.executemany('insert or replace into {0} values (?,?,?+coalesce((select v from {0} where k=? and c=?),0))'.format(self.tab),((k,c,v,k,c) for c,v in items))
	def delete(self,k,c=None): # TODO args: vgt vlt vge vle
		if c is None:
			self.conn.execute('delete from {0} where k=?'.format(self.tab),[k])
		else:
			self.conn.execute('delete from {0} where k=? and c glob ?'.format(self.tab),[k,c])
	def drop(self,tab=None):
		self.conn.execute('drop table if exists {0}'.format(tab or self.tab))
	### CORE - READ ###
	def get(self,k,c,default=None):
		x = self.conn.execute('select v from {0} where k=? and c=?'.format(self.tab),(k,c)).fetchone()
		return x[0] if x else default
	def items(self,k):
		return dict(self.iteritems(k))
	def scan(self,k='*',c='*',order=''):
		it = self.iterscan(k=k,c=c,order=order)
		for k,g in groupby(it,key=lambda x:x[0]):
			yield k,[(x[1],x[2]) for x in g] # or dict/ordered???
	def iterscan(self,k='*',c='*',order='',limit=-1): # TODO rename: scaniter? iscan?
		order_str = self.get_order_str(order)
		# TODO args: vgt vge vlt vle
		# TODO noglob
		# TODO from_c to_c
		# TODO from_k to_k
		# TODO partition p of P
		for k,c,v in self.conn.execute('select k,c,v from {0} where k glob ? and c glob ? {1} limit ?'.format(self.tab,order_str),(k,c,limit)):
			yield k,c,v
	def iteritems(self,k): # TODO rename: iitems?
		for c,v in self.conn.execute('select c,v from {0} where k=?'.format(self.tab),(k,)):
			yield c,v
		## for k,c,v in self.iterscan(k=k,limit=limit,order=order):
			## yield c,v
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
	### ADVANCED ###
	# TODO external database
	# TODO filter columns
	def to_col_store(self,arch_tab,keys_per_block=100): # TODO ser as arg
		import marshal
		from zlib import compress
		def ser(x): return buffer(compress(marshal.dumps(x,2)))
		#def ser(x): return buffer(marshal.dumps(x,2))
		#def ser(x): return unicode(x) # for debugging
		self.conn.execute("drop table if exists {0}".format(arch_tab))
		self.conn.execute("create table {0} (c,k,v)".format(arch_tab))
		col = None
		keys = []
		vals = []
		for k,c,v in self.conn.execute('select k,c,v from {0} order by c asc'.format(self.tab)):
			if len(keys)>=keys_per_block or col is not None and c!=col:
				self.conn.execute("insert into {0} values (?,?,?)".format(arch_tab),(col,ser(keys),ser(vals)))
				keys = []
				vals = []
			col = c
			keys.append(k)
			vals.append(v)
		if keys:
			self.conn.execute("insert into {0} values (?,?,?)".format(arch_tab),(col,ser(keys),ser(vals)))
	def to_col_store2(self,arch_tab,keys_per_block=100): # TODO ser as arg
		import marshal
		from zlib import compress
		def ser(x): return buffer(compress(marshal.dumps(x,2)))
		#def ser(x): return buffer(marshal.dumps(x,2))
		#def ser(x): return unicode(x) # for debugging
		self.conn.execute("drop table if exists {0}".format(arch_tab))
		self.conn.execute("create table {0} (c,k,v)".format(arch_tab))
		cols = []
		keys = []
		vals = []
		#for k,c,v in self.conn.execute('select k,c,v from {0} order by c asc'.format(self.tab)):
		for k,c,v in self.conn.execute('select k,c,v from {0}'.format(self.tab)):
			if len(keys)>=keys_per_block:
				## print('KEYS',keys)
				## print('COLS',cols)
				## print('VALS',vals)
				self.conn.execute("insert into {0} values (?,?,?)".format(arch_tab),(ser(cols),ser(keys),ser(vals)))
				cols = []
				keys = []
				vals = []
			cols.append(c)
			keys.append(k)
			vals.append(v)
		if keys:
			self.conn.execute("insert into {0} values (?,?,?)".format(arch_tab),(ser(cols),ser(keys),ser(vals)))
	# TODO external database
	# TODO filter columns
	def from_col_store(self,arch_tab):
		import marshal
		from zlib import decompress
		def de(x): return marshal.loads(decompress(x))
		#def de(x): return marshal.loads(x)
		#def de(x): return eval(x) # for debugging
		self.drop()
		self.create(index=False)
		for c,ser_keys,ser_vals in self.conn.execute('select c,k,v from {0}'.format(arch_tab)):
			keys = de(ser_keys)
			vals = de(ser_vals)
			self.conn.executemany('insert into {0} values (?,?,?)'.format(self.tab),((k,c,v) for k,v in zip(keys,vals)))
		self.create()
	def from_col_store2(self,arch_tab):
		import marshal
		from zlib import decompress
		def de(x): return marshal.loads(decompress(x))
		#def de(x): return marshal.loads(x)
		#def de(x): return eval(x) # for debugging
		self.drop()
		self.create(index=False)
		for ser_cols,ser_keys,ser_vals in self.conn.execute('select c,k,v from {0}'.format(arch_tab)):
			cols = de(ser_cols)
			keys = de(ser_keys)
			vals = de(ser_vals)
			## print('KEYS',keys)
			## print('COLS',cols)
			## print('VALS',vals)
			self.conn.executemany('insert into {0} values (?,?,?)'.format(self.tab),zip(keys,cols,vals))
		self.create()

# ------------------------------------------------------------------------------
if __name__=="__main__":
	db = KCV('usunmnie_kcv_x1.db')
	from time import time
	N = 100000
	C = 100
	data = []
	for k in range(N//C):
		for c in range(C):
			data.append([k,c,k*c])
	data2 = {}
	for k in range(N//C):
		data2[k] = {}
		for c in range(C):
			data2[k][c] = k*c
	t0=time()
	if 0:
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
	if 0: # 177k/s
		for k,c,v in data:
			db.set(k,c,v)
	if 1: # 334k/s
		for k in data2:
			items = data2[k].items()
			db.store(k,items)
	if 0: # 139k/s
		for k,c,v in data:
			db.incr(k,c,v)
	if 0: # 245k/s
		for k in data2:
			items = data2[k].items()
			db.incr_many(k,items)
	if 1: # unicode:500k/s marshal:640k/s zlib+marshal:300k/s
		t0=time()
		db.to_col_store('arch',1000)
	if 1: # eval:200k/s marshal:500k/s zlib+marshal:300k/s
		t0=time()
		db.from_col_store('arch')
	print(N/(time()-t0+0.0001))
	## for x in db.conn.execute('select * from arch limit 10'):
		## print(x)
	db.drop('main')
	db.sync(compact=True)
