class model5(object):
	def __init__(self):
		self.__chain__ = None
	def __getattribute__(self,x):
		if x.startswith('__') or x in ('chain',):
			return object.__getattribute__(self,x)
		if self.__chain__:
			v = self.__dict__[x] if x in self.__dict__ else getattr(self.__chain__,x)
		else:
			v = self.__dict__[x]
		return v() if callable(v) else v
	def __setattr__(self,x,y):
		object.__setattr__(self,x,y)
		if self.__chain__:
			object.__setattr__(self.__chain__,x,y)
	def chain(self,other):
		self.__chain__=other
		return self

if __name__=="__main__":
	x = model5()
	x.a = lambda: 20
	x.b = lambda: x.a+1
	print(x.a)
	print(x.b)
	y = model5()
	y.c = lambda: y.b*y.d
	y.chain(x)
	y.d = 2
	y.a = 0
	print(y.c)
