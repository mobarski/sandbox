import sqlite3
from pprint import pprint

def columnar(cursor):
	cols = [x[0] for x in cursor.description]
	c = [list() for _ in cols]
	for row in cursor:
		for i,val in enumerate(row):
			c[i] += [val]
	return dict(zip(cols,c))

db = sqlite3.connect('data.sqlite')

if 1:
	db.execute(''' drop table if exists link_em ''')
	db.execute(''' drop table if exists sat_user ''')
	db.execute(''' drop table if exists sat_format ''')
	db.execute(''' drop table if exists sat_user_agg ''')
	db.execute(''' drop table if exists sat_format_agg ''')

if 1: # INIT
	db.execute(''' create table if not exists link_em (day,user,platform,format,em_cnt,em_len) ''')
	db.execute(''' create table if not exists sat_user (user,grp,gender,offer,segment) ''')
	db.execute(''' create table if not exists sat_format (format,kind,category) ''')
	db.execute(''' create table if not exists sat_user_agg (user,em_cnt,em_len) ''')
	db.execute(''' create table if not exists sat_format_agg (format,users_cnt,em_cnt,em_len) ''')

if 1:
	db.execute(''' insert into link_em values ('2021-06-12','u1','p1','f1',1,2) ''')
	db.execute(''' insert into link_em values ('2021-06-12','u1','p1','f2',2,3) ''')
	db.execute(''' insert into link_em values ('2021-06-12','u2','p1','f1',2,4) ''')
	db.execute(''' insert into link_em values ('2021-06-12','u2','p2','f3',1,2) ''')
	db.execute(''' insert into sat_user values ('u1','a','m','o1','s1') ''')
	db.execute(''' insert into sat_user values ('u2','b','m','o1','s1') ''')
	db.execute(''' insert into sat_user values ('u4','a','f','o1','s1') ''')

rows = db.execute('''
	select
		day,
		sum(iif(grp=="a",em_len,0)) as a,
		sum(iif(grp=="b",em_len,0)) as b
	from link_em em
	left join sat_user u
	group by day
''')
pprint(columnar(rows))
