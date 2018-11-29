import sys; sys.path.append('..')
from v1 import *

t0=time()
n=128
nn=onn_layer(n*n,n*n,0.02)
clock('init',t0)
#print(nn.conn[0])
#print(nn.perm[0])
t0=time()
x=nn.save(open('../data/v1.marshal','wb'))
clock('save',t0)
print(x)
input = random_sparse_vector(100,200,n*n,0.02)
t0=time()
s = nn.score(input)
clock('score',t0)
#print(s)
t0=time()
nn.learn(input,100)
clock('learn',t0)

