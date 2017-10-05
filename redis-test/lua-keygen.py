from __future__ import print_function
import redis
from time import time,sleep
from multiprocessing import Pool

db = redis.StrictRedis('localhost')

N = 10000
db.delete('x_id','x_val_by_id','x_id_by_val')
keygen = db.register_script("""
local key_id
if redis.call("HEXISTS",KEYS[3],ARGV[1])>0 then
	key_id = redis.call("HGET",KEYS[3],ARGV[1])
else
	key_id = redis.call("INCR", KEYS[1])
	redis.call("HSET", KEYS[2], key_id, ARGV[1])
	redis.call("HSET", KEYS[3], ARGV[1], key_id)
end
return key_id
""")

def lua_keygen(val):
	return keygen(['x_id','x_val_by_id','x_id_by_val'],[val])

t0=time()
for i in range(N):
	val = str(i)*10
	keygen(['x_id','x_val_by_id','x_id_by_val'],[val])
t1=time()
print('serial keygen',' time {0:.2f}s'.format(t1-t0),' keys/s',int(N/(t1-t0)))
print(db.execute_command('memory usage x_val_by_id'))
print(db.execute_command('memory usage x_id_by_val'))


t0=time()
p=Pool(2)
list(p.map(lua_keygen,(str(i)*10 for i in range(N))))
t1=time()
print('parallel keygen',' time {0:.2f}s'.format(t1-t0),' keys/s',int(N/(t1-t0)))
