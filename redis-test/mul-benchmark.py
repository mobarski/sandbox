from __future__ import print_function
import redis
from time import time
from itertools import islice

# TODO - brakujace elementy - generowanie i obsluga

N = 10000
R = 30

def benchmark(fun, label='', R=5, cleaning_fun=lambda:0):
	times = []
	for i in range(R):
		t0=time()
		fun()
		dt=time()-t0
		times.append(dt)
		cleaning_fun()
	times.sort()
	min_t = int(1000*times[0])
	max_t = int(1000*times[-1])
	med_t = int(1000*times[len(times)//2])
	min_ips = int(N/times[-1]/1000)
	max_ips = int(N/times[0]/1000)
	med_ips = int(N/times[len(times)//2]/1000)
	min_rps = int(R/times[-1])
	max_rps = int(R/times[0])
	med_rps = int(R/times[len(times)//2])
	
	print('>        '+label)
	print('time ms    best:{0:<4}  median:{1:<4}  worst:{2}'.format(min_t, med_t, max_t))
	print('ops/s      best:{0:<4}  median:{1:<4}  worst:{2}'.format(max_rps, med_rps, min_rps))
	print('k items/s  best:{0:<4}  median:{1:<4}  worst:{2}'.format(max_ips, med_ips, min_ips))
	print()

	

db = redis.StrictRedis('localhost')
#db = redis.StrictRedis(unix_socket_path='/tmp/redis.sock')

# --- SETUP ---

db.delete('a')
db.delete('b')
db.delete('ha')
db.delete('hb')

a = {'k'+str(i):i for i in range(N)}
b = {'k'+str(i):i+1 for i in range(N)}

t0=time()
db.zadd('a',**a)
db.zadd('b',**b)
db.hmset('ha',a)
db.hmset('hb',b)
t1=time()

# --- BENCHMARK ---
print()
print('ITEMS   ',N)
print('RUNS    ',R)
print()

print('*** MULTIPLICATION *******************************************\n')

def python_mul():
	return {k:a[k]*b[k] for k in a if k in b}
benchmark(python_mul,
'two python dicts')


def interstore_mul_no_fetch():
	db.zinterstore('c',['a','b'],aggregate='mul')
benchmark(interstore_mul_no_fetch,
'two redis sorted sets multiplied in redis (aggregate mul), without fetching results')


def interstore_mul_fetch_100():
	db.zinterstore('c',['a','b'],aggregate='mul')
	return db.zrevrange('c',0,99,withscores=True)
benchmark(interstore_mul_fetch_100,
'two redis sorted sets multiplied in redis (aggregate mul), fetching top 100 kv pairs')


def interstore_mul():
	db.zinterstore('c',['a','b'],aggregate='mul')
	return dict(db.zscan_iter('c'))
benchmark(interstore_mul,
'two redis sorted sets multiplied in redis (aggregate mul)')


ss_mul = db.register_script('''
local resp
local out = {}
local key = 0
local cursor = 0
repeat
	resp = redis.call('zscan',KEYS[1],cursor)
	cursor = resp[1]
	for i,v in pairs(resp[2]) do
	  if i%2==1 then key=v
	  else
	    local x = redis.call('zscore',KEYS[2],key)
	    out[#out+1] = {key,v*x}
	  end
	end
until cursor=='0'
return out
''')
def lua_ss_mul():
	return ss_mul(['a','b'],[])
benchmark(lua_ss_mul,
'two redis sorted sets multiplied in lua')


ss_mul_into = db.register_script('''
redis.replicate_commands()
local resp
local key = 0
local cursor = 0
repeat
	resp = redis.call('zscan',KEYS[1],cursor)
	cursor = resp[1]
	for i,v in pairs(resp[2]) do
	  if i%2==1 then key=v
	  else
	    local x = redis.call('zscore',KEYS[2],key)
	    redis.call('zadd',KEYS[3],v*x,key)
	  end
	end
until cursor=='0'
''')
def lua_ss_mul_into_s():
	return ss_mul_into(['a','b','c'],[])
benchmark(lua_ss_mul_into_s,
'two redis sorted sets multiplied in lua, without fetching results')


def zscan_py_mul():
	aa = db.zscan_iter('a')
	return {k:aa[k]*b[k] for k in aa if k in b}
benchmark(zscan_py_mul,
'redis sorted set and python dict multiplied in python')


def hscan_py_mul():
	aa = db.hscan_iter('ha')
	return {k:aa[k]*b[k] for k in aa if k in b}
benchmark(zscan_py_mul,
'redis hash and python dict multiplied in python')



def zscan2_py_mul():
	aa = db.zscan_iter('a')
	bb = db.zscan_iter('b')
	return {k:aa[k]*bb[k] for k in aa if k in bb}
benchmark(zscan2_py_mul,
'two redis sorted sets multiplied in python')


def hscan2_py_mul():
	aa = db.hscan_iter('ha')
	bb = db.hscan_iter('hb')
	aa = {k:float(v) for k,v in aa}
	bb = {k:float(v) for k,v in bb}
	return {k:aa[k]*bb[k] for k in aa if k in bb}
benchmark(hscan2_py_mul,
'two redis hashes multiplied in python')


hash_mul = db.register_script('''
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
def lua_hash_mul():
	return hash_mul(['ha','hb'],[])
benchmark(lua_hash_mul,
'two redis hashes multiplied in lua')


print('*** HELPERS **************************************************\n')


hsum = db.register_script('''
local resp
local out = 0
local cursor = 0
repeat
	resp = redis.call('hscan',KEYS[1],cursor)
	cursor = resp[1]
	for i,v in pairs(resp[2]) do
	  if i%2==0 then
	    out = out + tonumber(v)
	  end
	end
until cursor=='0'
return out
''')
def lua_hsum():
	return hsum(['ha'],[])
benchmark(lua_hsum,
'lua hsum')


zsum = db.register_script('''
local resp
local out = 0
local cursor = 0
repeat
	resp = redis.call('zscan',KEYS[1],cursor)
	cursor = resp[1]
	for i,v in pairs(resp[2]) do
	  if i%2==0 then
	    out = out + v
	  end
	end
until cursor=='0'
return out
''')
def lua_zsum():
	return zsum(['a'],[])
benchmark(lua_zsum,
'lua zsum')


zlog = db.register_script('''
redis.replicate_commands()
local resp
local key = 0
local cursor = 0
repeat
	resp = redis.call('zscan',KEYS[1],cursor)
	cursor = resp[1]
	for i,v in pairs(resp[2]) do
	  if i%2==1 then key=v
	  else
	    redis.call('hset',KEYS[2],key,math.log(v))
	  end
	end
until cursor=='0'
''')
def lua_zlog():
	return zlog(['a','hx'],[])
benchmark(lua_zlog,
'lua zlog')


ztoh = db.register_script('''
redis.replicate_commands()
local resp
local key = 0
local cursor = 0
repeat
	resp = redis.call('zscan',KEYS[1],cursor)
	cursor = resp[1]
	for i,v in pairs(resp[2]) do
	  if i%2==1 then key=v
	  else
	    redis.call('hset',KEYS[2],key,v)
	  end
	end
until cursor=='0'
''')
def lua_ztoh():
	return ztoh(['a','ha2'],[])
benchmark(lua_ztoh,
'lua ztoh')


htoz = db.register_script('''
redis.replicate_commands()
local resp
local key = 0
local cursor = 0
repeat
	resp = redis.call('hscan',KEYS[1],cursor)
	cursor = resp[1]
	for i,v in pairs(resp[2]) do
	  if i%2==1 then key=v
	  else
	    redis.call('zadd',KEYS[2],v,key)
	  end
	end
until cursor=='0'
''')
def lua_htoz():
	return htoz(['ha','a2'],[])
benchmark(lua_htoz,
'lua htoz')

print('*** PRODUCT **********************************************\n')


def set_mul_lua_sum_prod():
	db.zinterstore('c',['a','b'],aggregate='mul')
	return zsum(['c'],[])
benchmark(set_mul_lua_sum_prod,
'two redis sorted sets multiplied in redis (aggregate mul), sum calculated in lua')


ss_prod = db.register_script('''
local resp
local out = 0
local key = 0
local cursor = 0
repeat
	resp = redis.call('zscan',KEYS[1],cursor)
	cursor = resp[1]
	for i,v in pairs(resp[2]) do
	  if i%2==1 then key=v
	  else
	    local x = redis.call('zscore',KEYS[2],key)
	    out = out + v*x
	  end
	end
until cursor=='0'
return out
''')
def lua_ss_prod():
	return ss_prod(['a','b'],[])
benchmark(lua_ss_prod,
'two redis sorted sets product calculated in lua')



hh_prod = db.register_script('''
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
def lua_hh_prod():
	return hh_prod(['ha','hb'],[])
benchmark(lua_hh_prod,
'two redis hashes product calculated in lua')



sh_prod = db.register_script('''
local resp
local out = 0
local key = 0
local cursor = 0
repeat
	resp = redis.call('zscan',KEYS[1],cursor)
	cursor = resp[1]
	for i,v in pairs(resp[2]) do
	  if i%2==1 then key=v
	  else
	    local x = redis.call('hget',KEYS[2],key)
	    out = out + v*tonumber(x)
	  end
	end
until cursor=='0'
return out
''')
def lua_sh_prod():
	return sh_prod(['a','hb'],[])
benchmark(lua_sh_prod,
'redis sorted set and redis hash product calculated in lua')



hs_prod = db.register_script('''
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
	    local x = redis.call('zscore',KEYS[2],key)
	    out = out + tonumber(v)*x
	  end
	end
until cursor=='0'
return out
''')
def lua_hs_prod():
	return hs_prod(['ha','b'],[])
benchmark(lua_hs_prod,
'redis hash and redis sorted set product calculated in lua')





