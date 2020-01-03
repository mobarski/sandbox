import sqlite3

sql = 'create table zzz (aaa JSON)'

sql = 'select info1,count(*) from xxx group by info1'
sql = 'select count(*) from xxx'
sql = 'select * from xxx where aspect like "%,%" limit 36'
sql = 'select * from xxx where flex="fin" limit 36'
sql = 'select flex,count(*) from xxx where pos=="czasownik" group by flex'
sql = 'select info2,count(*) from xxx group by info2'

db = sqlite3.connect('multi9.sqlite')
for x in db.execute(sql):
	print(x)
