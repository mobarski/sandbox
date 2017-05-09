class model:
	## core ##############################################
	def __getattribute__(self,x):
		v = object.__getattribute__(self,x)
		return v(self) if callable(v) and x not in ['copy','update'] else v
	## aux ##############################################
	def update(self,other):
		for k,v in other.__dict__.items():
			self.__dict__[k]=v
		return self
	def copy(self):
		m = model()
		return m.update(self)

if __name__=="__main__":
	m = model()
	m.a = lambda m: m.r
	m.v = lambda m: (2*m.u/m.r - m.u/m.a)**0.5
	m.r = 10
	m.u = 123
	z = m.copy()
	print(z.v)
