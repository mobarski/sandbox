import sqlite3

class DB:
	def __init__(self):
		self.dir = "../data"
		self.part = {}
	
	def get_part(self, name):
		if name not in self.part:
			con = sqlite3.connect(f"{self.dir}/{name}.sqlite")
			self.part[name] = con
		return self.part[name]
	
if __name__=="__main__":
	db = DB()
	#p = db.get_part('2021-08-09')
	#p.execute('create table if not exists xxx (a,b,c)')
	#p.executemany('insert into xxx values (?,?,?)',[(11,21,31),(41,51,61),(71,81,91)])
	#p.commit()
	mem = sqlite3.connect(':memory:')
	for i,day in enumerate(['2021-08-09','2021-08-10']):
		p = db.get_part(day)
		rows = p.execute(f"select *,'{day}' as day from xxx")
		cols = [x[0] for x in rows.description]
		if i==0:
			cols_args = ",".join(["?" for _ in cols])
			cols_str = ",".join(cols)
			mem.execute('drop table if exists agg')
			mem.execute(f'create table agg ({cols_str})')
		mem.executemany(f'insert into agg values ({cols_args})',rows)
	print(list(mem.execute('select * from agg')))

	
