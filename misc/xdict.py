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

class xdict2(dict):
	__slots__ = ('__dict__','__getattr__','__setattribute__')
	def __init__(self,*a,**kw):
		dict.__init__(self,*a,**kw)
		self.__getattr__ = self.__getitem__
		self.__setattribute__ = self.__setitem__
