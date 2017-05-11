import operator
import math

"""
numpy and pandas inspired array object with python native numeric types
"""

def is_array(x):
	return hasattr(x,'__getitem__')
	
def fun1(f,x):
	return array([f(xi) for xi in x]) if is_array(x) else f(x)

# SANDBOX
class pipe1:
	def __init__(self,f):
		self.f=f
	def __call__(self,x):
		f=self.f
		return array([f(xi) for xi in x]) if is_array(x) else f(x)
	def __or__(self,x):
		print('or',x)

class array(list):
	def op(self,op,other): # handle self on the left side of the operator: self+other
		for i in range(len(self)):
			x = other[i] if is_array(other) else other
			self[i] = op(self[i],x)
		return self
	def rop(self,op,other): # handle self on the right side of the operator: other+self
		for i in range(len(self)):
			x = other[i] if is_array(other) else other
			self[i] = op(x,self[i])
		return self

	def __add__(self,other): return self.op(operator.add,other)
	def __mul__(self,other): return self.op(operator.mul,other)
	def __div__(self,other): return self.op(operator.div,other)
	def __truediv__(self,other): return self.op(operator.truediv,other)
	def __sub__(self,other): return self.op(operator.sub,other)
	def __mod__(self,other): return self.op(operator.mod,other)
	def __pow__(self,other): return self.op(operator.pow,other)
	def __lshift__(self,other): return self.op(operator.lshift,other)
	def __rshift__(self,other): return self.op(operator.rshift,other)

	def __radd__(self,other): return self.rop(operator.add,other)
	def __rmul__(self,other): return self.rop(operator.mul,other)
	def __rdiv__(self,other): return self.rop(operator.div,other)
	def __rtruediv__(self,other): return self.rop(operator.truediv,other)
	def __rsub__(self,other): return self.rop(operator.sub,other)
	def __rmod__(self,other): return self.rop(operator.mod,other)
	def __rpow__(self,other): return self.rop(operator.pow,other)
	def __rlshift__(self,other): return self.rop(operator.lshift,other)
	def __rrshift__(self,other): return self.rop(operator.rshift,other)

	def __lt__(self,other): return self.op(operator.lt,other)
	def __gt__(self,other): return self.op(operator.gt,other)
	def __le__(self,other): return self.op(operator.le,other)
	def __ge__(self,other): return self.op(operator.ge,other)
	def __eq__(self,other): return self.op(operator.eq,other)
	def __ne__(self,other): return self.op(operator.ne,other)

def arange(*args):
	return(array(range(*args)))
def linspace(start, stop, num=50, endpoint=True):
	n = num-1 if endpoint else num
	step = (stop-start)/n
	return array([start+i*step for i in range(num)])
def linspace2(start,stop,step=1,endpoint=True):
	num = int(math.floor((stop-start)/step))
	num += 1 if endpoint else 0
	return array([start+i*step for i in range(num)])
#def logspace(start, stop, num=50, endpoint=True, base=10.0): pass # TODO

pi=math.pi
e=math.e
nan=float('nan')
inf=oo=float('inf')
to_rad=math.radians
to_deg=math.degrees

_abs=abs
_int=int
def abs(x): return fun1(_abs,x)
def int(x): return fun1(_int,x)
def exp(x): return fun1(math.exp,x)
def log(x): return fun1(math.log,x)
def log10(x): return fun1(math.log10,x)
def cos(x): return fun1(math.cos,x)
def sin(x): return fun1(math.sin,x)
def tan(x): return fun1(math.tan,x)
def atan(x): return fun1(math.atan,x)
def asin(x): return fun1(math.asin,x)
def acos(x): return fun1(math.acos,x)
def erf(x): return fun1(math.erf,x)
def erfc(x): return fun1(math.erfc,x)
def gamma(x): return fun1(math.gamma,x)
def lgamma(x): return fun1(math.lgamma,x)

if __name__=="__main__":	
	print(linspace2(0,10,2))




