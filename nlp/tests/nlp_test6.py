import sys; sys.path.append('..')

from nlp import *
from cache import *
from frame import *

from time import time
from collections import Counter

if __name__=="__main__":
	cache = disk_cache('../cache/v6',verbose=True,linear=True)
	
	t0 = time()
	X = cache.get('vectorized')
	Y = cache.get('col')
	vocab = cache.get('vocab')
	print('vocab',len(vocab))

	#from array import array
	#frame = dict(X=[array('H',x) for x in X],Y=Y)
	#frame = dict(X=X,Y=Y)
	#cache.set_map('test_frame',frame)

	#x1 = filtered(X,Y,lambda y:y=='parenting')
	x1 = X
	if 0:
		for x in x1:
			#print(x.keys())
			#print([vocab[t] for t in x.keys()])
			print(x)
			print([vocab[t] for t in x])
			print
	if 0:
		co = get_co(x1,triangular=False,diagonal=True,stream=True,symetry=True,ngram_max=5)
		cache.set('co',dict(co))
	co = cache.get('co')
	
	for (v1,v2),f in Counter(co).most_common(200):
		print(v1,v2,f,vocab[v1],vocab[v2])
	print(time()-t0)
	print(len(co))
	t0=time()
	co2 = {}
	for v1,v2 in co:
		if v1 not in co2:
			co2[v1] = Counter()
		co2[v1][v2] = co[v1,v2]
	print(time()-t0)
	
	exit()
	
	t1 = 'ios'
	V1 = vocab.index(t1)
	v1 = V1
	for v2,cnt in co2[v1].most_common(10):
		print(v1,vocab[v1],vocab[v2],cnt)
	
	t2 = 'gra'
	V2 = vocab.index(t2)
	v2 = V2
	for v1,cnt in co2[v2].most_common(10):
		print(v2,vocab[v2],vocab[v1],cnt)

	v1,v2 = V1,V2

	n = 200
	a = dict(co2[v1].most_common(n))
	b = dict(co2[v2].most_common(n))
	c = {}
	for t in a:
		if t not in b: continue
		c[t] = a[t]*b[t]
	for x,v in Counter(c).most_common(40):
		print(vocab[x],v)
