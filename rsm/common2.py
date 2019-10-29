from __future__ import print_function
import numpy as np
from random import shuffle
from time import time
from heapq import nlargest

import marshal

def combinations(n,k):
	"return k from n combination"
	out = list(range(n))
	shuffle(out)
	return out[:k]

def random_vector(n,lo,hi):
	"return 1d uniform random vector"
	return np.random.randint(lo,hi+1,n)

def top(k,d,items=False,values=False):
	"return k elements with largest values from dictionary"
	if items:
		return nlargest(k,((x,d[x]) for x in d),key=lambda x:x[1])
	elif values:
		return nlargest(k,d.values())
	else:
		return nlargest(k,d,key=lambda x:d[x])

def clock(label,t0,t1=None):
	"print execution time"
	dt = time()-t0 if t1==None else t1-t0
	print("{:.3f}\t{}".format(dt,label))

if __name__=="__main__":
	x = random_vector(30,0,1)
	print(x)
	y = random_vector(30,0,1)
	print(y)
	print(x+y)
	print(combinations(10,5))
	d = dict(enumerate(x+y))
	print(top(3,d))
	
