import numpy as np
from sklearn.decomposition import NMF

#X = np.array([[1,1,1],[1,0,1],[0,2,1],[1,2,0]])
X = [[1,1,1],[1,0,1],[0,2,1],[1,2,0]]
model = NMF(3)
W = model.fit_transform(X)
H = model.components_
print(W)
print(H)


