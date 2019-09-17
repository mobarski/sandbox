import sqlite3
from functools import partial
import multiprocessing as mp

def create(args):
	p,name,sql = args
	db = sqlite3.connect(name)
	db.execute(sql)	

class mydb:
	def __init__(self, w):
		self.pool = mp.Pool(w)
	
	def create(self, tab, name_tmpl, parts=[0]):
		sql = 'create table if not exists {}'.format(tab)
		args = [(p,name_tmpl.format(p),sql) for p in parts]
		self.pool.map(create,args)
	
	def insert_iter(self): pass # TODO API

if __name__ == "__main__":
	db = mydb(4)
	db.create('main(a,b,c)','data/v4_{}.sqlite',[1,2,3,4,5])
