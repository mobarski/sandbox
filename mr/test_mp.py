import multiprocessing as mp
import sqlite3
from time import time

def initializer():
	global db
	db = sqlite3.connect('data/all')

def worker(x):
	return db.execute("select * from test where text like '%a%'").fetchall()

if __name__=="__main__":
	t0=time()
	pool = mp.Pool(2,initializer)
	out = pool.map(worker, list(range(100)))
	print(out)
	print(time()-t0)
