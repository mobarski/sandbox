from __future__ import print_function

import numpy as np
from  scipy.sparse.linalg import svds
from vectorize import X,F

XA = X.toarray().astype(float)
u,s,v = svds(XA,3)

print(u)
print(s)
print(v)

for topic in v:
	print()
	for w,t in sorted(zip(topic,F),reverse=True):
		if w<0.001: continue
		print(t,w)
