class namespace: pass
class model(object):
	def __init__(self):
		self.__chain__ = None
	def __getattribute__(self,x):
		if x.startswith('__') or x in ('chain','items'):
			return object.__getattribute__(self,x)
		v = self.__dict__[x] if x in self.__dict__ else self.__chain__.__dict__[x]
		return v() if callable(v) else v
	def __setattr__(self,x,y):
		if x.startswith('__'):
			object.__setattr__(self,x,y)
		elif x in self.__dict__:
			self.__dict__[x]=y
		else:
			self.__chain__.__dict__[x]=y
	def chain(self,other):
		self.__chain__=other
		return self
	def items(self):
		return [(k,getattr(self,k)) for k in self.__dict__]

if 1:
	x = model()
	x.a = lambda: 20
	x.b = lambda: x.a+1
	print(x.a)
	print(x.b)
	y = model()
	y.a = 0
	y.c = lambda: y.b*y.d
	y.d = 2
	y.chain(x)
	print(y.c)
	print(y.items())

###

class model(object):
	def __getattribute__(self,x):
		if x.startswith('__') or x in ('chain','items'):
			return object.__getattribute__(self,x)
		v = self.__dict__[x]
		return eval(v,self.__dict__) if isinstance(v,str) else v
	def chain(self,other):
		self.__dict__.update(other.__dict__)
		return self

if 0:
	x = model()
	x.a = 20
	x.b = 'a+1'
	y = model().chain(x)
#	y.a = 0
	y.c = 'b*d'
	y.d = 2
	print(y.c)
