# encoding: UTF-8

# Wide Column Store (Key-Column-Value database) built on top of SQLite
# (c) 2017 by mobarski (at) gmail (dot) com
# licence: MIT
# version: x1m3 (x-experimental, p-preview, r-release, m-modification)

# x1m6 - better test coverage
# x1m5 - tests, limit_str, some comments, set_items<-store, scan_items(cast=
# x1m4 - delete as scan(), __enter__
# x1m3 - col_store in external file, col_store order, ser/de as args, where_str, scan_col_store
# x1m2 - incr_many,benchmark,limit,delete,sync,to_col_store(x2),from_col_store(x2)

from __future__ import print_function
import sqlite3
from itertools import groupby

class KCV:
	"Wide Column Store built on top of SQLite"
	def __init__(self, path=':memory:', tab='main'):
		# TODO readonly mode
		self.path = path
		self.tab = tab
		self.conn = sqlite3.connect(path)
		self.create()
		
	def create(self,index=True):
		self.conn.execute('create table if not exists {0} (k,c,v)'.format(self.tab))
		if index:
			self.conn.execute('create unique index if not exists i_{0} on {0} (k,c)'.format(self.tab))
	
	def execute(self,*a,**kw):
		"execute sql statement - for debugging"
		print('EXECUTE',*a,**kw)
		return self.conn.execute(*a,**kw)
	
	def __enter__(self):
		return self
	
	def __exit__(self, ex_type, ex_val, ex_tb):
		if ex_type is None:
			self.sync()
	
	### WRITE ###
	
	def sync(self,compact=False):
		if compact:
			self.conn.execute('vacuum')
		self.conn.commit()
		
	def set(self,k,c,v):
		self.conn.execute('insert or replace into {0} values (?,?,?)'.format(self.tab),(k,c,v))
		
	def set_items(self,k,items):
		self.conn.executemany('insert or replace into {0} values (?,?,?)'.format(self.tab),((k,c,v) for c,v in items))
		
	def incr(self,k,c,v=1):
		self.conn.execute('insert or replace into {0} values (?,?,?+coalesce((select v from {0} where k=? and c=?),0))'.format(self.tab),(k,c,v,k,c))
		
	def incr_items(self,k,items):
		self.conn.executemany('insert or replace into {0} values (?,?,?+coalesce((select v from {0} where k=? and c=?),0))'.format(self.tab),((k,c,v,k,c) for c,v in items))
	
	def delete(self,k,c='*',**kw):
		list(self.scan(mode='delete',k=k,c=c,**kw)) # list() required as scan is an iterator

	def drop(self,tab=None):
		self.conn.execute('drop table if exists {0}'.format(tab or self.tab))
	
	### READ ###
	
	def get(self,k,c,default=None):
		x = self.conn.execute('select v from {0} where k=? and c=?'.format(self.tab),(k,c)).fetchone()
		return x[0] if x else default
	
	def items(self,k):
		return {c:v for k,c,v in self.scan(k=k)}
	
	def scan_items(self,k='*',c='*',order='',cast=list,**kw):
		it = self.scan(k=k,c=c,order=order,**kw)
		for k,g in groupby(it,key=lambda x:x[0]):
			yield k,cast(((x[1],x[2]) for x in g))
	
	def scan(self,k='*',c='*',order='',limit=None,mode='kcv',**kw):
		select_str,select_cnt = self.get_select_str(mode)
		where_str,where_vals = self.get_where_str(k,c,kw)
		order_str = self.get_order_str(order)
		limit_str,limit_vals = self.get_limit_str(limit)
		sql = '{0} from {1} {2} {3} {4}'.format(select_str, self.tab, where_str, order_str, limit_str)
		if select_cnt>1:
			for row in self.conn.execute(sql, where_vals+limit_vals):
				yield row
		else:
			for [row] in self.conn.execute(sql, where_vals+limit_vals):
				yield row

	def join(self): pass # TODO (LATER: x2) JOIN left,inner sum,min,max,mul,?prod

	def agg(self): pass # TODO (LATER: x3) AGG sum,max,min,count,count distinct,count null,count range
	
	### SQL CODE GENERATION UTILS ###
	
	def get_limit_str(self,limit):
		if limit is None: return '',[]
		else: return 'limit ?',[limit]
	
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

	def get_select_str(self,mode):
		if mode=='kcv': return 'select k,c,v',3
		if mode=='kc': return 'select distinct k,c',2
		if mode=='k': return 'select distinct k',1
		if mode=='c': return 'select distinct c',1
		if mode=='delete': return 'delete',0

	def get_where_str(self,k,c,kw):
		# TODO - better arg names
		# TODO - like (case insensitive)
		# TODO - regexp (custom function)
		# TODO - match (custom function)
		sql,val = [],[]
		
		if k!='*':
			try:
				if '*' in k or '?' in k or '[' in k:
					sql.append('k glob ?'); val.append(k)
				else:
					sql.append('k=?'); val.append(k)
			except TypeError:
				sql.append('k=?'); val.append(k)
		if c!='*':
			try:
				if '*' in c or '?' in c or '[' in c:
					sql.append('c glob ?'); val.append(c)
				else:
					sql.append('c=?'); val.append(c)
			except TypeError:
				sql.append('c=?'); val.append(c)
		
		if 'klt' in kw: sql.append('k<?'); val.append(kw['klt'])
		if 'clt' in kw: sql.append('c<?'); val.append(kw['clt'])
		if 'vlt' in kw: sql.append('v<?'); val.append(kw['vlt'])
		
		if 'kgt' in kw: sql.append('k>?'); val.append(kw['kgt'])
		if 'cgt' in kw: sql.append('c>?'); val.append(kw['cgt'])
		if 'vgt' in kw: sql.append('v>?'); val.append(kw['vgt'])

		if 'kle' in kw: sql.append('k<=?'); val.append(kw['kle'])
		if 'cle' in kw: sql.append('c<=?'); val.append(kw['cle'])
		if 'vle' in kw: sql.append('v<=?'); val.append(kw['vle'])

		if 'kge' in kw: sql.append('k>=?'); val.append(kw['kge'])
		if 'cge' in kw: sql.append('c>=?'); val.append(kw['cge'])
		if 'vge' in kw: sql.append('v>=?'); val.append(kw['vge'])

		# LIMIT - sqlite3 limits queries to 999 variables ('?' placeholders)
		if 'kin' in kw: sql.append('k in ({0})'.format((',?'*len(kw['kin']))[1:])); val.extend(kw['kin'])
		if 'cin' in kw: sql.append('c in ({0})'.format((',?'*len(kw['cin']))[1:])); val.extend(kw['cin'])
		if 'vin' in kw: sql.append('v in ({0})'.format((',?'*len(kw['vin']))[1:])); val.extend(kw['vin'])
		
		if sql:
			return 'where '+' and '.join(sql),val
		else:
			return '',[]
	
	### ADVANCED - COLUMNAR ARCHIVE ###
	
	def to_col_store(self,path,batch=1000,tab='arch',order='',ser=None,move=False,k='*',c='*',**kw):
		"archive table into compressed, columnar storage in external file"
		if ser is None:
			import marshal
			from zlib import compress
			def ser(x): return buffer(compress(marshal.dumps(x,2)))
		arch_conn = sqlite3.connect(path)
		arch_conn.execute("drop table if exists {0}".format(tab))
		arch_conn.execute("create table {0} (c,k,v)".format(tab))
		where_str,where_vals = self.get_where_str(k,c,kw)
		order_str = self.get_order_str(order)
		cols = []
		keys = []
		vals = []
		for k,c,v in self.conn.execute('select k,c,v from {0} {1} {2}'.format(self.tab, where_str, order_str),where_vals):
			if len(keys)>=batch:
				arch_conn.execute("insert into {0} values (?,?,?)".format(tab),(ser(cols),ser(keys),ser(vals)))
				if move:
					self.conn.executemany("delete from {0} where k=? and c=?".format(self.tab),zip(keys,cols))
				cols = []
				keys = []
				vals = []
			cols.append(c)
			keys.append(k)
			vals.append(v)
		if keys:
			arch_conn.execute("insert into {0} values (?,?,?)".format(tab),(ser(cols),ser(keys),ser(vals)))
		arch_conn.execute('vacuum')
		arch_conn.commit()
		arch_conn.close()
	
	def from_col_store(self, path, tab='arch', de=None, merge=False):
		"restore table from archive kept in external file"
		if de is None:
			import marshal
			from zlib import decompress
			def de(x): return marshal.loads(decompress(x))
		arch_conn = sqlite3.connect(path)
		if not merge:
			self.drop()
			self.create(index=False)
		for ser_cols,ser_keys,ser_vals in arch_conn.execute('select c,k,v from {0}'.format(tab)):
			cols = de(ser_cols)
			keys = de(ser_keys)
			vals = de(ser_vals)
			self.conn.executemany('insert into {0} values (?,?,?)'.format(self.tab),zip(keys,cols,vals))
		if not merge:
			self.create()

	def scan_col_store(self,path,tab='arch',de=None):
		"iterate over table in external archive file"
		if de is None:
			import marshal
			from zlib import decompress
			def de(x): return marshal.loads(decompress(x))
		arch_conn = sqlite3.connect(path)		
		for ser_cols,ser_keys,ser_vals in arch_conn.execute('select c,k,v from {0}'.format(tab)):
			cols = de(ser_cols)
			keys = de(ser_keys)
			vals = de(ser_vals)
			for k,c,v in zip(keys,cols,vals):
				yield k,c,v

