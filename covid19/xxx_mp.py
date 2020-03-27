import multiprocessing as mp
from time import time
from tqdm import tqdm

def worker(x):
	from time import sleep
	sleep(2)
	return x*x

if __name__=="__main__":
	data = list(range(20))
	pool = mp.Pool(processes=4)

	t0=time()
	total = 0

	if 0:
		r = pool.map(worker,data)	
	if 0:
		r = pool.map(worker,tqdm(data))
	if 1:
		r = pool.imap(worker,data)
	if 0:
		r = pool.imap(worker,tqdm(data)) # to nie ma sensu -> tqdm powinien byc na wyniku
		
	print(f't_map {time()-t0:.02f}')
	for x in tqdm(r, desc='testing', total=len(data)):
		print(f't_x {time()-t0:.02f}')
		total += x

	print(f'done in {time()-t0:.0f} seconds')
	print(total)
