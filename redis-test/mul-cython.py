from __future__ import print_function
from time import time
import pyximport; pyximport.install()

N = 1000000
R = 10

a = {'k'+str(i):i for i in range(N)}
b = {'k'+str(i):i+1 for i in range(N)}

def run():
	x={k:a[k]*b[k] for k in a if k in b}
	## for k in a:
		## if k not in b: continue
		## a[k]*b[k]
t0=time()
run()
t1=time()
print('cython mul',' time {0:.2f}s'.format(t1-t0),' op/s',int(N/(t1-t0)))
