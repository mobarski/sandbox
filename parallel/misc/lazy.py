if 0:
	import itertools
	def flat_map(f,iter):
		return itertools.chain.from_iterable(map(f,iter))
	print(list(flat_map(lambda x:x,[[1],[2],[],[3,4]])))

def __call__(f,a_kw):
	a,kw=a,kw
	return f(*a,**kw)

def __pipe__(a,b):
	return a(b)

import operator as op
class lazy:
	def __init__(self):
		self.ops = []
	
	def __call__(self,x):
		for f,other in self.ops:
			x = f(x,other)
		return x
	
	def __getattr__(self,x):
		self.ops += [(op.attrgetter,x)]
		return self
	def __getitem__(self,x):
		self.ops += [(op.getitem,x)]
		return self
	#~ def __call__(self,*a,**kw):
		#~ x = (a,kw)
		#~ self.ops += [(__call__,x)]
		#~ return self		
	
	# operators: + - / * % **
	def __add__(self,x):
		self.ops += [(op.add,x)]
		return self
	def __sub__(self,x):
		self.ops += [(op.sub,x)]
		return self
	def __mul__(self,x):
		self.ops += [(op.mul,x)]
		return self
	def __div__(self,x):
		self.ops += [(op.div,x)]
		return self
	def __mod__(self,x):
		self.ops += [(op.mod,x)]
		return self
	def __pow__(self,x):
		self.ops += [(op.pow,x)]
		return self
	
	# operators: > < <= => == !=
	def __lt__(self,x):
		self.ops += [(op.lt,x)]
		return self
	def __gt__(self,x):
		self.ops += [(op.gt,x)]
		return self
	def __le__(self,x):
		self.ops += [(op.le,x)]
		return self
	def __ge__(self,x):
		self.ops += [(op.ge,x)]
		return self
	def __eq__(self,x):
		self.ops += [(op.eq,x)]
		return self
	def __ne__(self,x):
		self.ops += [(op.ne,x)]
		return self
	
	# other
	def __or__(self,x):
		self.ops += [(__pipe__,x)]
		return self
	
class base:
	def __add__(self,x): return lazy()+x
	def __gt__(self,x): return lazy()>x
	
	
_=base()
print(list(map(_>5,[1,3,5,7,9])))

