from __future__ import print_function
import redis
from time import time

db = redis.StrictRedis('localhost')

N = 100000

db.delete('a')
db.delete('b')

a = {'k'+str(i):i for i in range(N)}
b = {'k'+str(i):i+1 for i in range(N)}

t0=time()
db.zadd('a',**a)
db.zadd('b',**b)
t1=time()

#~ print('zadd*2',' time {0:.2f}s'.format(t1-t0),' op/s',int(N/(t1-t0)))
#~ print(db.execute_command('MEMORY USAGE a'))
#~ print(db.execute_command('MEMORY USAGE b'))

t0=time()
x={k:a[k]*b[k] for k in a if k in b}
t1=time()
print('python mul',' time {0:.2f}s'.format(t1-t0),' op/s',int(N/(t1-t0)))

t0=time()
db.zinterstore('c',['a','b'],aggregate='mul')
t1=time()
print('zinterstore mul',' time {0:.2f}s'.format(t1-t0),' op/s',int(N/(t1-t0)))

t0=time()
aa = db.zscan_iter('a')
bb = db.zscan_iter('b')
x={k:aa[k]*bb[k] for k in aa if k in bb}
t1=time()
print('zscan py mul',' time {0:.2f}s'.format(t1-t0),' op/s',int(N/(t1-t0)))
