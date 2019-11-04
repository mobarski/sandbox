from rsm import test1,test2,test3
import numpy as np
from time import time as perf_counter

N = 40
M = 20
V = 20


mem = np.zeros((N,M), dtype=np.int32)
neg = np.zeros((N,V), dtype=np.int32)
out = np.zeros(N, dtype=np.int32)
input = np.zeros(M,  dtype=np.int32)

input[0]=1
for i in range(1,M):
	input[i] = i*10

test1(mem,input)

# test 2

a=test2(mem,input,out)
print(out)
print(a)

R=10000
t0=perf_counter()
for i in range(R):
	test2(mem,input,out)
dt=perf_counter()-t0
print(1.0*R/dt)

# test3 -> 5x szybszy dla N=40

out.fill(0)
test3(mem,input,out)
print(out)

R=10000
t0=perf_counter()
for i in range(R):
	test3(mem,input,out)
dt=perf_counter()-t0
print(1.0*R/dt)
