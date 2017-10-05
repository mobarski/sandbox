from __future__ import print_function
import redis
from time import time,sleep
from multiprocessing import Pool

db = redis.StrictRedis('localhost')

N = 40000



# return cjson.encode({ARGV[1],42})
# return cmsgpack.pack({ARGV[1],42})

#db.delete('x_id','x_val_by_id','x_id_by_val')
hashgen = db.register_script('''
return redis.sha1hex(ARGV[1])
''')

def lua_hash(s):
	return hashgen([],[s])

print(hashgen([],['xxx']))
print(lua_hash('xxx'))

t0=time()
for i in range(N):
	val = str(i)*10
	hashgen([],[val])
t1=time()
print('serial sha',' time {0:.2f}s'.format(t1-t0),' op/s',int(N/(t1-t0)))

t0=time()
p=Pool(2)
list(p.map(lua_hash,(str(i)*10 for i in range(N))))
t1=time()
print('parallel sha',' time {0:.2f}s'.format(t1-t0),' op/s',int(N/(t1-t0)))
