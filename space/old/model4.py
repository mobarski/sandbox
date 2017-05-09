class model4:
	def __getattr__(self,x):
		var_name = 'var_'+x
		v = self.__dict__[var_name] if var_name in self.__dict__ else self.__dict__[x]
		return v() if callable(v) else v
	def chain(self,other):
		for k,v in other.__dict__.items():
			self.__dict__[k]=v
		return self

if __name__=="__main__":
	x = model4()
	x.var_a = lambda: 20
	x.var_b = lambda: x.a+1
	y = model4().chain(x)
	y.var_c = lambda: y.b*y.d
	y.d = 2
	print(y.c)
