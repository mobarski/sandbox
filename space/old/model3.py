class model3(object):
	def __getattribute__(self,x):
		if x.startswith('__') or x in ('chain',):
			return object.__getattribute__(self,x)
		v = self.__dict__[x]
		return v() if callable(v) else v
	def chain(self,other):
		self.__dict__.update(other.__dict__)
		return self

if __name__=="__main__":
	x = model3()
	x.a = lambda: 20
	x.b = lambda: x.a+1
	print(x.b)
	y = model3().chain(x)
	y.c = lambda: y.b*y.d
	y.d = 2
	print(y.c)
