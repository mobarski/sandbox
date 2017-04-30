from const import *
class float_obj(float): pass

# TODO units

## EX3 ########################

class formula:
	def __init__(self,hint,**formulas):
		self.hint=hint
		self.formula=formulas
	def copy(self):
		f = formula(self.hint,**self.formula)
		f.__dict__=self.__dict__.copy()
		return f
	def expand(self,x):
		return self.formula[x].replace('{','({').replace('}','})').format(**self.__dict__)
	def __getattr__(self,x):
		return eval(self.expand(x))

if __name__=="__main__":
	f=formula("circular orbit velocity",
		v='({u}/{r})**0.5',
		u='{r}*{v}**2',
		r='{u}/{v}**2')

	f.u='GM.sun'
	f.r='D.earth + 400e3'
	f1=f.copy()
	print(f1.u)
	print(f)
	print(f.expand('v'))
	print(f.v)
	
	v_circ = formula("circular orbit velocity",
		v='({u}/{r})**0.5',
		u='{r}*{v}**2',
		r='{u}/{v}**2')

	v_elip = formula("elipse orbit velocity",
		v='(2*{u}/{r}-{u}/{a})**0.5',
		u='{r}*{v}**2',
		r='{u}/{v}**2')

	print(v_elip.formula['v'])
	