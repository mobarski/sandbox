import sqlite3
import marshal
import array
import struct

db = sqlite3.connect('test.db')

db.execute('drop table if exists test')
db.execute('create table if not exists test (x,y)')

data = []
for i in range(1000):
	x = 2**60-i
	rec = [x,marshal.dumps([x]*1024*2)]
	data.append(rec)
db.executemany('insert into test values (?,?)',data)
db.commit()
