import multiprocessing as mp
import sqlite3

# IDEA:
# - baza partycjonowana po czasie oparta o sqlite
# - partycja obslugiwana w osobnym, rownoleglym procesie
# - map -> zapytania sql wewnatrz partycji
# - combine -> za pomoca sqla lub pythona
# - reduce -> za pomoca pythona

# v2 - dowolny schemat zamiast kcv

def worker(id,pipe):
	_db = sqlite3.connect('test_p{}.sqlite'.format(id))
	db = _db.cursor()
	while True:
		msg = pipe.recv()
		if msg[0] == 'quit':
			break
		elif msg[0] == 'execute':
			sql = msg[1]
			values = msg[2] if len(msg)>2 else None
			db.execute(sql)#,values)
		
		elif msg[0] == 'set':
			table = msg[1]
			values = msg[2]
			holders = ','.join(['?']*len(values))
			db.execute('insert or replace into {} values ({})'.format(table,holders),values)
			
		elif msg[0] == 'table':
			name = msg[1]
			cols = ','.join(msg[2:])
			db.execute('create table if not exists {} ({})'.format(name,cols))
		elif msg[0] == 'unique index':
			table = msg[1]
			cols = ','.join(msg[2:])
			name = 'iu_'+table
			db.execute('create unique index if not exists {} on {} ({})'.format(name,table,cols))
			
		
		elif msg[0] == 'get':
			table = msg[1]
			where = msg[2]
			values = msg[3]
			out = []
			for x in db.execute('select * from {} where {}'.format(table,where),values):
				out += [x]
			pipe.send(out)

		elif msg[0] == 'count':
			table = msg[1]
			where = msg[2]
			out = next(db.execute('select count(*) from {} where {}'.format(table,where)))[0]
			pipe.send(out)
	
		elif msg[0] == 'items':
			k = msg[1]
			out = ['resp']
			for x in db.execute('select c,v from main where k=?',[k]):
				out += [x]
			pipe.send(out)


class Pool:
	def __init__(self,n):
		self.n = n
		self.workers = {}
		self.pipes = {}
		
		for i in range(n):
			id = i+1
			p1,p2 = mp.Pipe()
			w = mp.Process(target=worker,args=[id,p1])
			self.workers[id] = w
			self.pipes[id] = p2
			
		self.start()
	
	def start(self):
		for id,w in self.workers.items():
			w.start()
	
	def close(self):
		for id,p in self.pipes.items():
			p.send(['quit'])
		for id,w in self.workers.items():
			w.join()
	
	def execute(self,id,sql,values=[]):
		self.pipes[id].send(['execute',sql,values])
	
	def execute_all(self,sql,values=[]):
		for p in self.pipes.values():
			p.send(['execute',sql,values])
	
	
	
	def set(self,id,table,values):
		self.pipes[id].send(['set',table,values])
	
	def get(self,id,table,where,values=[]):
		self.pipes[id].send(['get',table,where,values])
		return self.pipes[id].recv()

	def count(self,id,table,where):
		self.pipes[id].send(['count',table,where])
		return self.pipes[id].recv()


if __name__=="__main__":
	from gen import random_rec
	from time import time
	
	N = 1000000
	W = 12
	
	
	data = []
	for i in range(N):
		rec = random_rec([(1,10),(2,10),(3,10),(1,100),(2,100),(3,100),(1,1000),(2,1000),(3,1000),(1,10000),(2,10000),(3,10000)])
		data += [(i,[i+1]+rec)]
	
	p = Pool(W)
	p.execute_all('create table if not exists test (k,a1,a2,a3,b1,b2,b3,c1,c2,c3,d1,d2,d3)')
	p.execute_all('create unique index if not exists iu_test on test (k)')
	t0 = time()
	for i,rec in data:
		p.set(1+(i%W),'test',rec)
	print(time()-t0)
	print(1.0*N/(time()-t0))

	t0 = time()	
	for id in p.workers:
		print(id,p.count(id,'test','b1=42'))
	print(time()-t0)
	print(1.0*N/(time()-t0))

	
	p.close()
	
