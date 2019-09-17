import multiprocessing as mp
import sqlite3

# IDEA:
# - baza partycjonowana po czasie oparta o sqlite
# - partycja obslugiwana w osobnym, rownoleglym procesie
# - map -> zapytania sql wewnatrz partycji
# - combine -> za pomoca sqla lub pythona
# - reduce -> za pomoca pythona

# v0 - bez sqlite, struktura w RAM ala REDIS

def worker(id,pipe):
	db = {}
	while True:
		msg = pipe.recv()
		if msg[0] == 'quit':
			break
		elif msg[0] == 'set':
			k = msg[1]
			v = msg[2]
			db[k] = v
		elif msg[0] == 'get':
			k = msg[1]
			out = db.get(k)
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
	
	def set(self,id,key,val):
		self.pipes[id].send(['set',key,val])
	
	def get(self,id,key):
		self.pipes[id].send(['get',key])
		return self.pipes[id].recv()


if __name__=="__main__":
	from gen import random_rec
	from time import time
	db = {}
	N = 80000
	W = 4
	
	p = Pool(W)
	
	data = []
	for i in range(N):
		rec = random_rec([(1,100000),  (1,10),(2,10),(3,10),(1,100),(2,100),(3,100),(1,1000),(2,1000),(3,1000),(1,10000),(2,10000),(3,10000)])
		data += [rec]
		
	t0 = time()
	for rec in data:
		#p.set(1+i%W,rec[0],rec[1:])
		db[rec[0]] = rec[1:]
	
	print(time()-t0)
	print(1.0*N/(time()-t0))
	
	p.close()
	