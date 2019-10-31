from __future__ import print_function
import numpy as np
from random import shuffle, random
from time import time
from heapq import nlargest
from collections import deque

import marshal
from pprint import pprint

def combinations(n,k):
	"return k from n combination"
	out = list(range(n))
	shuffle(out)
	return out[:k]

def random_vector(n,lo=0,hi=1):
	"return 1d uniform random vector"
	return np.random.randint(lo,hi+1,n)

def random_sparse_vector(n,lo=0,hi=1,d=0.1,k=None):
	"return 1d random vector with some of its values set to zero"
	sparse = np.zeros(n)
	k = k or int(d*n)
	positions = combinations(n,k)
	sparse[list(positions)] = random_vector(k,lo+1,hi)
	return sparse

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

def avg(v):
	"average"
	return 1.0*sum(v)/len(v)

def pick(v_set,n):
	"select n random values from a set"
	if n<=0: return []
	out = list(v_set)
	shuffle(out)
	return out[:n]

if __name__=="__main__":
	x = random_vector(30,0,1)
	print(x)
	y = random_vector(30,0,1)
	print(y)
	print(x+y)
	print(combinations(10,5))
	d = dict(enumerate(x+y))
	print(top(3,d,values=True))
	print(top(2,dict(a=1,b=2,c=3),values=True))
	print(top(2,dict(a=1,b=2,c=3),values=False))
	print(random_sparse_vector(20,d=0.2))
	print(random_sparse_vector(20,k=10))
