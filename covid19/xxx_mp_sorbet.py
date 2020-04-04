import multiprocessing as mp
from multiprocessing.pool import ThreadPool
from time import time
from tqdm import tqdm
from horacy.sorbet import sorbet
from random import randint

def worker(doc):
	for i in range(0,randint(0,doc['x']+1)):
		doc['x'] += 1
	return doc

if __name__=="__main__":
	pool = mp.Pool(processes=4)
	#pool = ThreadPool(processes=4)

	s1 = sorbet('usunmnie/s1').dump([dict(x=i) for i in range(20_000)])
	s2 = sorbet('usunmnie/s2').new()

	t0=time()
	total = 0

	if 0:
		r = pool.map(worker,s1)	
	if 0:
		r = pool.map(worker,tqdm(s1))
	if 1:
		r = pool.imap(worker,s1)
	if 0:
		r = pool.imap(worker,tqdm(s1)) # to nie ma sensu -> tqdm powinien byc na wyniku
	if 0:
		r = map(worker,s1)
		
	print(f't_map {time()-t0:.02f}')
	for doc in r:
		s2.append(doc)
	s2.save()

	print(f'done in {time()-t0:.03f} seconds')

	for i in range(10):
		print(s2[i])
	print(len(s2))