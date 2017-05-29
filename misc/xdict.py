class xdict(dict):
	"""
	>>> d = xdict(one=1,two=2)
	>>> d.one
	1
	>>> d.two
	2
	>>> d.not_five = 3
	>>> d.not_five
	3
	"""
	def __getattr__(self,x):
		return self[x]
	def __setattr__(self,x,v):
		self[x] = v
