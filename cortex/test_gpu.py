import numpy as np
import numba
from numba import cuda

a = np.array([1,2,3,4,5])
b = np.array([1,2,3,4,5])
c = np.zeros_like(a)

print(a,b,c)

@cuda.jit('void(int32[:],int32[:],int32[:])')
def xyz(x,y,z):
	i = cuda.grid(1)
	z[i] = x[i] * y[i]

xyz(a,b,c)
print(c)
