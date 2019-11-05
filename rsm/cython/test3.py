from rsm import scores,learn_positive,learn_negative
import numpy as np
from time import time as perf_counter

N = 5
M = 7
I = 5
V = 9

mem = np.zeros((N,M), dtype=np.int32)
hit = np.zeros((N,M), dtype=np.int32)
used = np.zeros(N, dtype=np.int32)
mem=np.sort(mem,axis=1)
neg = np.zeros((N,V), dtype=np.int32)
out = np.zeros(N, dtype=np.int32)
input = np.zeros(I, dtype=np.int32)

input[0]=1
for i in range(1,I):
	input[i] = i*5
print(input)

mem[0,0] = 10
mem[1,0] = 1
mem[1,1] = 30
mem[2,0] = 5
mem[2,1] = 15
mem[2,2] = 25
used[0] = 1
used[1] = 2
used[2] = 3
print(mem)

learn_positive(mem,neg,input,out,used,hit,dropout=0.0,k=4)
print(mem)
print(used)
print(hit)

input = np.array([1,10,20],dtype=np.int32)
learn_negative(mem,neg,input,out,used,hit,dropout=0.0,k=4)
print(mem)
print(used)
print(neg)

input = np.array([1,6,11,16,25,30],dtype=np.int32)
learn_negative(mem,neg,input,out,used,hit,dropout=0.0,k=4)
print(mem)
print(used)
print(neg)

input = np.array([2,3,4,5,6,7],dtype=np.int32)
learn_negative(mem,neg,input,out,used,hit,dropout=0.0,k=4)
print(mem)
print(used)
print(neg)