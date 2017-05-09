class model2:
	def __getattr__(self,x):
		v = self.__dict__[x]
		return v() if callable(v) else v
	def chain(self,other):
		self.__dict__.update(other.__dict__)
		return self

if __name__=="__main__":
	x = model2()
	x.a = lambda: 20
	x.b = lambda: x.a+1
	y = model2().chain(x)
	y.c = lambda: y.b*2
	print(y.c)
