import sys; sys.path.append('..')
from v1 import *

t0=time()
NI = 10
NN = 500
nn=onn_layer(NI,NN,0.5)

X1 = [random_vector(1,255,NI) for _ in range(10)]
X2 = [random_vector(1,255,NI) for _ in range(10)]

t0=time()
for i in range(10):
	for x in X1:
		nn.learn(x,5)
clock('learn',t0)
for x in X1:
	print(dict_top(nn.score(x),3))
print
for x in X2:
	print(dict_top(nn.score(x),3))
