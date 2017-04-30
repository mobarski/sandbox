from const import *
class float_obj(float): pass

## EX2 ########################

class formula(float):
	def set(self,**formulas):
		self.__formulas__=formulas
		return self
	def copy(self):
		f = formula().set(**self.__formulas__)
		f.__dict__=self.__dict__.copy()
		return f
	def expand(self,x):
		return self.__formulas__[x].format(**self.__dict__)
	def __getattr__(self,x):
		result = float_obj(eval(self.expand(x)))
		result.explain = x+'='+self.expand(x)
		result.formula = x+'='+self.__formulas__[x].replace('{','').replace('}','')
		return result

f=formula().set(
	v='({u}/{r})**0.5',
	u='{r}*{v}**2',
	r='{u}/{v}**2')

f.u='GM.sun'
f.r='D.earth'
print(f.v.explain)
print(f.v.formula)
f1=f.copy()
print(f1.u)
