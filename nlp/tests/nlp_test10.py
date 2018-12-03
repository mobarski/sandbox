from __future__ import print_function
import sys; sys.path.append('..')
from nlp import *

"""
test #10 - shingling
"""

X = [
"to jest test a to jest test ale inny czyli eksperyment",
"zupelnie inne zdanie, ktore ma zupelnie inne zadanie bo to jest test",
"to jest eksperyment a to jest zupelnie inne zadanie",
]

def shingle(x):
	return list(map(hash,x))

if __name__=="__main__":

	V = vectorize(X,vocabulary=None,stream=True,ngram_range=(2,3),postprocessor2=None)
	for v in V:
		print(v)
	print()
	
	inv_idx = {}
	for i,v in enumerate(V):
		for t in v:
			if t not in inv_idx: inv_idx[t] = set()
			inv_idx[t].add(i)
	for t in inv_idx:
		if len(inv_idx[t])==1: continue
		print(t,inv_idx[t])
