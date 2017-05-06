class model(object):
	def __init__(self,doc=""):
		self.__doc__=doc # TODO
	def __getattribute__(self,x):
		if x.startswith('__') or x in ('update',):
			return object.__getattribute__(self,x)
		v = self.__dict__[x]
		return v(self) if callable(v) else v
	def update(self,other):
		self.__dict__.update(other.__dict__)
		return self

if __name__=="__main__":
	x = model('first')
	x.a = lambda x: 20
	x.b = lambda x: x.a+1
	print(x.a)
	print(x.b)
	y = model('second').update(x)
	y.c = lambda y: y.b*y.d
	#y.update(x)
	y.d = 2
	y.a = 0
	print(y.c)
	print(y.b)
	help(x)
