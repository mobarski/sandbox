from const import *

## EX4 ########################

class formula:
	def __init__(self,hint,info='',**formulas):
		self.hint=hint
		self.info=info
		self.formula=formulas
	def copy(self):
		f = formula(self.hint,**self.formula)
		f.__dict__=self.__dict__.copy()
		return f
	def expand(self,x):
		f = self.formula[x]
		while '{' in f:
			f = f.replace('{','({').replace('}','})').format(**self.__dict__)
		return f
	def __getattr__(self,x):
		return eval(self.expand(x))

if __name__=="__main__":
	f=formula("eliptical orbit velocity",
		"""
		v = (2*u/r - u/a)**0.5
		v -> eliptical orbit velocity [m/s]
		u -> central body mass constant equal to G*M [m3/s2]
		r -> distance to focus [m]
		a -> semi-major axis [m]
		""",
		v='(2*{u}/{r} - {u}/{a})**0.5',
		u='',
		r='',
		a='')

	f.u='GM.earth'
	f.r='D.earth + 400e3'
	f.a='{r}'
	print(f.expand('v'))

	f=formula('midified gas law',
		"""
		p = rho * R * T
		p -> pressure [N/m2]
		rho -> density [kg/m3]
		R -> specific gas constant 'R'/M [J/(kg*K)]
		T -> temperature [K]
		""",
		p = '{rho} * {R} * {T}',
		rho = '{p} / ({R}*{T})',
		T = '{p} / ({rho}*{R})'
		)
		