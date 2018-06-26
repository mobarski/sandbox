from __future__ import print_function

import numpy as np
from sklearn.decomposition import PCA
from vectorize import X,F

XA = X.toarray().astype(float)
pca = PCA(3)
y = pca.fit_transform(XA)
z = pca.components_

print(y)
print(z)

for topic in z:
	print()
	for w,t in sorted(zip(topic,F),reverse=True):
		if w<0.001: continue
		print(t,w)
