class DT:
	"""datatable inspired interface to SQLite"""
	def __init__(self,table_name,db=None):
		self.table_name = table_name
		self.join = '' # TODO
		self.db = db
	def __getitem__(self,a):
		if not type(a) is tuple:
			a = (a,)
		select = a[0]
		rest = ' '.join(a[1:])
		sql = """select {} from {} {}""".format(select, self.table_name, rest)
		print(sql) # XXX
		if self.db:
			return self.db.execute(sql) # TODO placeholders
		else:
			return sql
	def columns(self):
		return [] # TODO

d=DT('costam.moja_tabela')
d['x,sum(y),sum(z)','where a>10 group by x','limit 10']
