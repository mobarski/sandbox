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

v_elip = formula("elipse orbit velocity",
	v='(2*{u}/{r}-{u}/{a})**0.5',
	u='{r}*{v}**2',
	r='{u}/{v}**2')
