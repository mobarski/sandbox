import numpy as np
from random import shuffle
from time import time
import marshal
from heapq import nlargest

def combinations(n,k):
	k = k if type(k)==int else int(k*n)
	if k < 0.3*n: # TODO - optimize threshold
		out = set(np.random.randint(0,n,k))
		while len(out)<k:
			missing_cnt = k-len(out)
			out.update(np.random.randint(0, n, missing_cnt))
	else:
		out = list(range(n))
		shuffle(out)
		return set(out[:k])
	return out

def random_vector(lo,hi,n):
	return np.random.randint(lo,hi,n)

def random_sparse_vector(lo,hi,n,d=0.1):
	sparse = np.zeros(n)
	k = int(d*n)
	positions = combinations(n,k)
	sparse[list(positions)] = random_vector(lo,hi,k)
	return sparse 

def clock(label,t0,t1=None):
	"print execution time"
	dt = time()-t0 if t1==None else t1-t0
	print("{:.3f}\t{}".format(dt,label))

def top(k,d,items=False,values=False):
	if items:
		return nlargest(k,((x,d[x]) for x in d),key=lambda x:x[1])
	elif values:
		return nlargest(k,d.values())
	else:
		return nlargest(k,d,key=lambda x:d[x])
