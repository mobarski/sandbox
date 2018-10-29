from time import time
from nlp import get_dfy,get_df_from_dfy,get_df,vectorize

docs = [
'xxx to jest test aaa',
'yyy a to jest cos innego bbb',
'zzz ciekawe co to jest ccc',
'xxx to nie test to sprawdzenie aaa',
'yyy jak zwal tak zwal bbb',
'zzz ciekawe co bedzie dalej ccc',
]

N = 200000
if __name__=="__main__":
	import numpy as np
	import marshal
	import pickle
	dfy = get_dfy(docs,[0,0,0,1,1,1])
	print(dfy)
	df = get_df_from_dfy(dfy)
	print(df.most_common(100))
	df = get_df(docs)
	print(df.most_common(100))
	vocabulary = sorted(df.keys())
	print(vocabulary)
	xdocs=docs*N
	t0 = time()
	v = vectorize(xdocs,vocabulary=vocabulary,sparse=True,binary=False,typecode=None,dtype=None,upper_limit=1)#dtype=np.uint8)
	#v = vectorize(xdocs,vocabulary=vocabulary,sparse=False,binary=True,typecode='B')
	if N<=100:
		print(v)
	print(time()-t0)
	t0=time()
	print('marshal',len(marshal.dumps(v)),time()-t0)
	#t0=time()
	#print('pickle',len(pickle.dumps(v,2)),time()-t0)
