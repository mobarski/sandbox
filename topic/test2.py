from contrib import *

db = redis.StrictRedis('127.0.0.1',db=7)
p = proton(db,2)
print(db.keys())
