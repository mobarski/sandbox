from __future__ import print_function
import redis
from time import time,sleep
from multiprocessing import Pool

db = redis.StrictRedis('localhost')

mul = db.register_script('''
local resp
local out = {}
local key = 0
local cursor = 0
repeat
	resp = redis.call('hscan',KEYS[1],cursor)
	cursor = resp[1]
	for i,v in pairs(resp[2]) do
	  if i%2==1 then key=v
	  else
	    local x = redis.call('hget',KEYS[2],key)
	    out[#out+1] = {key,tonumber(v)*tonumber(x)}
	  end
	end
until cursor=='0'
return out
''')

t0=time()
out = mul(['ha','hb'],[])
t1=time()
print('lua mul',t1-t0,len(out),len(out)/(t1-t0))


prod = db.register_script('''
local resp
local out = 0
local key = 0
local cursor = 0
repeat
	resp = redis.call('hscan',KEYS[1],cursor)
	cursor = resp[1]
	for i,v in pairs(resp[2]) do
	  if i%2==1 then key=v
	  else
	    local x = redis.call('hget',KEYS[2],key)
	    out = out + tonumber(v)*tonumber(x)
	  end
	end
until cursor=='0'
return out
''')

t0=time()
out2 = prod(['ha','hb'],[])
t1=time()
print('lua prod',t1-t0,len(out),len(out)/(t1-t0))
