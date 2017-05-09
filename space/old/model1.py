class model1:
	def __getattr__(self,x):
		getter = 'var_'+x
		if getter in self.__dict__:
			return self.__dict__[getter]()
		else:
			return self.__dict__[x]
	def chain(self,other):
		for k,v in other.__dict__.items():
			self.__dict__[k]=v
		return self

if __name__=="__main__":
	x = model1()
	x.var_a = lambda: 20
	x.var_b = lambda: x.a+1
	y = model1().chain(x)
	y.var_c = lambda: y.b*2
	print(y.c)
