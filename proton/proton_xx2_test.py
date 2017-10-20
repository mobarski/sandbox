from proton_x2 import proton
from time import sleep
import redis

def handler(id):
	print('handling id',id)
	sleep(1)
	return 'done'

db = redis.StrictRedis('localhost')
col = 'test'
db.sadd(col+':all','a','b','c','d','e','f','g','h','i','j','k','l','m','n')
db.delete(col+':done')
db.sdiffstore(col+':todo',col+':all',col+':done') # budowa TODO


p = proton(db,2)
resp = p.loop(handler,['test']*4)
print(resp)