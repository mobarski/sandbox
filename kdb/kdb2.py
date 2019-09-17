import sqlite3

def sanitize(x):
	return x

class KDB:
	def __init__(self,db):
		self.db = db
	#
	def create(self,*keys):
		for key in keys:
			key = sanitize(key)
			self.execute('create table if not exists {} (k primary key) without rowid'.format(key))
	def drop(self,*keys):
		for key in keys:
			key = sanitize(key)
			self.execute('drop table if exists {}'.format(key))
	def keys(self):
		pass
	#	
	def union(self,*keys):
		keys = [sanitize(key) for key in keys]
		sql = ' union '.join(['select k from {}'.format(key) for key in keys])
		return (x[0] for x in self.execute(sql))
	def diff(self,*keys):
		keys = [sanitize(key) for key in keys]
		sql = 'select t0.k from {} t0'.format(keys[0])
		for i,k in enumerate(keys[1:]):
			t = 't{}'.format(i+1)
			sql += ' left join {} {} on {}.k==t0.k'.format(k,t,t)
		sql += ' where '
		sql += ' or '.join(['t{}.k is null'.format(i) for i in range(1,len(keys))])
		return (x[0] for x in self.execute(sql))
	def inter(self,*keys):
		keys = [sanitize(key) for key in keys]
		sql = 'select t0.k from {} t0'.format(keys[0])
		for i,k in enumerate(keys[1:]):
			t = 't{}'.format(i+1)
			sql += ' inner join {} {} on {}.k==t0.k'.format(k,t,t)
		return (x[0] for x in self.execute(sql))
	def card(self,key):
		key = sanitize(key)
		sql = 'select count(*) from {}'.format(key)
		return self.execute(sql).fetchall()[0][0]
	def members(self,key):
		key = sanitize(key)
		sql = 'select k from {}'.format(key)
		return (x[0] for x in self.execute(sql))
	#
	def add(self,key,*vals):
		return self.add_iter(key,vals)
	def add_iter(self,key,values):
		key = sanitize(key)
		return self.executemany('insert or replace into {} values (?)'.format(key),[[v] for v in values])
	def remove(self,key,*vals): pass
	def remove_iter(self,key,values): pass
	#
	def inter_store(self,key,*keys): pass
	def diff_store(self,key,*keys): pass
	def union_store(self,key,*keys): pass
	def pop(self): pass # TODO
	def move(self): pass # TODO
	#
	def execute(self,sql,args=[]):
		print(sql)
		return self.db.execute(sql,args)
	def executemany(self,sql,args=[]):
		return self.db.executemany(sql,args)


if __name__=="__main__":
	db = sqlite3.connect(':memory:')
	kdb = KDB(db)
	kdb.create('aa','bb','cc')
	kdb.add('aa',123,456,789)
	kdb.add('bb',12,456,789)
	kdb.add('cc',23,56,789)
	print(list(kdb.members('aa')))
	x=kdb.inter('aa','bb','cc')
	print(list(x))
	x=kdb.union('aa','bb','cc')
	print(list(x))
	x=kdb.diff('aa','bb')
	print(list(x))
	print(kdb.card('aa'))