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

if __name__=="__main__":
	import numpy as np
	dfy = get_dfy(docs,[0,0,0,1,1,1])
	print(dfy)
	df = get_df_from_dfy(dfy)
	print(df.most_common(100))
	df = get_df(docs)
	print(df.most_common(100))
	features = sorted(df.keys())
	print(features)
	xdocs=docs*200000
	t0 = time()
	v = vectorize(xdocs,features=features,sparse=False,binary=True,dtype=np.uint8)
	#v = vectorize(xdocs,features=features,sparse=False,binary=True,typecode='B')
	print(time()-t0)
	#print(v) # xxx
	