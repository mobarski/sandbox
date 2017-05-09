class model6(object):
	def __init__(self,doc=""):
		self.doc=doc
	def __getattribute__(self,x):
		if x.startswith('__') or x in ('update',):
			return object.__getattribute__(self,x)
		v = self.__dict__[x]
		return v(self) if callable(v) else v
	def update(self,other):
		self.__dict__.update(other.__dict__)
		return self

if __name__=="__main__":
	x = model6()
	x.a = lambda x: 20
	x.b = lambda x: x.a+1
	print(x.a)
	print(x.b)
	y = model6().update(x)
	y.c = lambda y: y.b*y.d
	#y.update(x)
	y.d = 2
	y.a = 0
	print(y.c)
	print(y.b)
