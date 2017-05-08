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

if 0:
	x = model1()
	x.var_a = lambda: 20
	x.var_b = lambda: x.a+1
	y = model1().chain(x)
	y.var_c = lambda: y.b*2
	print(y.c)

####################################################

class model2:
	def __getattr__(self,x):
		v = self.__dict__[x]
		return v() if callable(v) else v
	def chain(self,other):
		self.__dict__.update(other.__dict__)
		return self

if 0:
	x = model2()
	x.a = lambda: 20
	x.b = lambda: x.a+1
	y = model2().chain(x)
	y.c = lambda: y.b*2
	print(y.c)

####################################################

class model3(object):
	def __getattribute__(self,x):
		if x.startswith('__') or x in ('chain',):
			return object.__getattribute__(self,x)
		v = self.__dict__[x]
		return v() if callable(v) else v
	def chain(self,other):
		self.__dict__.update(other.__dict__)
		return self

if 0:
	x = model3()
	x.a = lambda: 20
	x.b = lambda: x.a+1
	print(x.b)
	y = model3().chain(x)
	y.c = lambda: y.b*y.d
	y.d = 2
	print(y.c)

####################################################

class model4:
	def __getattr__(self,x):
		var_name = 'var_'+x
		v = self.__dict__[var_name] if var_name in self.__dict__ else self.__dict__[x]
		return v() if callable(v) else v
	def chain(self,other):
		for k,v in other.__dict__.items():
			self.__dict__[k]=v
		return self

if 0:
	x = model4()
	x.var_a = lambda: 20
	x.var_b = lambda: x.a+1
	y = model4().chain(x)
	y.var_c = lambda: y.b*y.d
	y.d = 2
	print(y.c)

####################################################

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

if 0:
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


####################################################

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

if 0:
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

####################################################

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

if 1:
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
	
