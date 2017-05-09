class model7:
	def __getattr__(self,x):
		var_name = x+'_fun'
		v = self.__dict__[x] if x in self.__dict__ else self.__dict__[var_name]
		return v(self) if callable(v) else v
	def chain(self,other):
		for k,v in other.__dict__.items():
			self.__dict__[k]=v
		return self
	def reset(self):
		attributes = [k for k in self.__dict__ if not k.endswith('_fun')]
		for a in attributes:
			del self.__dict__[a]

if __name__=="__main__":
	x = model7()
	x.a_fun = lambda x: 20
	x.b_fun = lambda x: x.a+1
	y = model7().chain(x)
	y.c_fun = lambda y: y.b*y.d
	y.d = 2
	print(y.c)
	z = model7()
	z.b_fun = lambda x:x.a
	z.a_fun = lambda x:x.b
	z.b=1
	print(z.a)
