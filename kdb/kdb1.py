# key only database

import sqlite3

class KDB:
	def __init__(self,db,table):
		self.db = db
		self.table = table.replace('.','_')
		self.create()
	def create(self):
		sql = 'create table if not exists {} (k primary key)'.format(self.table)
		self._execute(sql)
		
	def add(self,v):
		sql = 'insert or replace into {} values (?)'.format(self.table)
		self._execute(sql,v)
	def update(self,values):
		sql = 'insert or replace into {} values (?)'.format(self.table)
		self._executemany(sql,values)
	def keys(self):
		sql = 'select k from {} order by k'.format(self.table)
		return (x[0] for x in self._execute(sql))
	
	def _execute(self,sql,*args):
		return self.db.execute(sql,args)
	def _executemany(self,sql,args):
		return self.db.executemany(sql,[[x] for x in args])

if __name__=="__main__":
	db = sqlite3.connect(':memory:')
	kdb = KDB(db,'xx')
	kdb.add('xxx')
	kdb.add('yyy')
	kdb.add('zzz')
	kdb.update(['xxx','aaa','bbb','zzz'])
	print(list(kdb.keys()))
