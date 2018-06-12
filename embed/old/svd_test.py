import numpy as np
from  scipy.sparse.linalg import svds

X = np.array([[1,1,1,0],[1,0,1,2],[0,2,1,1],[1,2,0,1]],dtype=float)

u,s,v = svds(X,3)
print(u)
print(s)
print(v)
