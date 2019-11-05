from rsm import scores
import numpy as np
from time import time as perf_counter

N = 20
M = 20
V = 20


mem = np.random.randint(1,100,size=(N,M), dtype=np.int32)
hit = np.zeros((N,M), dtype=np.int32)
used = np.zeros(N, dtype=np.int32)
mem=np.sort(mem,axis=1)
neg = np.zeros((N,V), dtype=np.int32)
out = np.zeros(N, dtype=np.int32)
input = np.zeros(M,  dtype=np.int32)

input[0]=1
for i in range(1,M):
	input[i] = i*5

a=scores(mem,input,out)
print(out)
print(a)

R=10000
t0=perf_counter()
for i in range(R):
	scores(mem,input,out)
dt=perf_counter()-t0
print(1.0*R/dt)

print(mem)


