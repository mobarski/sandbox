from __future__ import print_function

import numpy as np
from sklearn.decomposition import FastICA as ICA
from vectorize import X,F


model = ICA(4)
W = model.fit_transform(X.toarray())
H = model.components_

print(W) # doc->topic
print(H) # topic->word

for topic in H:
	print()
	for w,t in sorted(zip(topic,F),reverse=True):
		if w<0.001: continue
		print(t,w)
