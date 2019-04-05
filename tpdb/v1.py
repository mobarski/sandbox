import multiprocessing as mp
import sqlite3

# IDEA:
# - baza partycjonowana po czasie oparta o sqlite
# - partycja obslugiwana w osobnym, rownoleglym procesie
# - map -> zapytania sql wewnatrz partycji
# - combine -> za pomoca sqla lub pythona
# - reduce -> za pomoca pythona

def worker(id,pipe):
	db = sqlite3.connect('test_p{}.sqlite'.format(id))
	db.execute('create table if not exists main (k,c,v)')
	db.execute('create unique index if not exists i_main on main (k,c)')
	while True:
		msg = pipe.recv()
		if msg[0] == 'quit':
			break
		elif msg[0] == 'set':
			k = msg[1]
			c = msg[2]
			v = msg[3]
			db.execute('insert or replace into main values (?,?,?)',[k,c,v])
		elif msg[0] == 'get':
			k = msg[1]
			c = msg[2]
			out = ['resp']
			for x in db.execute('select v from main where k=? and c=?',[k,c]):
				out += [x[0]]
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
	
	def set(self,id,key,col,val):
		self.pipes[id].send(['set',key,col,val])
	
	def get(self,id,key,col):
		self.pipes[id].send(['get',key,col])
		return self.pipes[id].recv()

	def items(self,id,key):
		self.pipes[id].send(['items',key])
		return self.pipes[id].recv()


if __name__=="__main__":
	p = Pool(2)
	
	p.set(1,'key1','col1',111)
	p.set(1,'key1','col2',222)
	p.set(2,'key1','col1',333)
	p.set(2,'key1','col2',444)
	
	print(p.get(1,'key1','col1'))
	print(p.get(2,'key1','col1'))
	print(p.items(1,'key1'))
	print(p.items(2,'key1'))
	
	p.close()
	
