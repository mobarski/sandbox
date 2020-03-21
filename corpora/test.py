import sqlite3

db=sqlite3.connect('freq.sqlite')
sql = "select count(*) from freq where key=='SC1'"
sql = "select * from freq where key=='SC2' limit 90"
sql = "select sum(freq) from freq"
sql = "create table agg as select * from (select token,sum(freq) as freq group by token) order by freq desc, token asc"

#db.execute('drop table if exists agg')
sql = "create table agg as select token,sum(freq) as freq from freq group by token order by 2 desc, 1 asc"
sql = "select rowid,* from agg where token like 'd%' limit 10"
for x in db.execute(sql):
	print(x)
db.commit()

