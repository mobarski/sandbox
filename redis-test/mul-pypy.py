from __future__ import print_function
from time import time

N = 1000000

a = {'k'+str(i):i for i in range(N)}
b = {'k'+str(i):i+1 for i in range(N)}

t0=time()
x={k:a[k]*b[k] for k in a if k in b}
t1=time()
print('pypy mul',' time {0:.2f}s'.format(t1-t0),' op/s',int(N/(t1-t0)))
