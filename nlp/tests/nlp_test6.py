import sys; sys.path.append('..')

from nlp import *
from cache import *
from frame import *

from time import time

if __name__=="__main__":
	cache = disk_cache('../cache','t5v2',verbose=True,linear=True)
	
	t0 = time()
	X = cache.get('vectorized')
	Y = cache.get('col')
	vocab = cache.get('vocab')
	print('vocab',len(vocab))

	x1 = filtered(X,Y,lambda y:y=='parenting')
	if 0:
		for x in x1:
			#print(x.keys())
			#print([vocab[t] for t in x.keys()])
			print(x)
			print([vocab[t] for t in x])
			print
	co1 = get_co(x1,triangular=True,diagonal=False,stream=True,ngram_max=2)
	for (v1,v2),f in Counter(co1).most_common(200):
		print(v1,v2,f,vocab[v1],vocab[v2])
	print(time()-t0)

