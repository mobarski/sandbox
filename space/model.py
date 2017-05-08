class model:
	"""
	"""
	def __getattr__(self,x):
		fun_name = x+'_fun'
		v = self.__dict__[x] if x in self.__dict__ else self.__dict__[fun_name]
		return v(self) if callable(v) else v
	def chain(self,other):
		for k,v in other.__dict__.items():
			self.__dict__[k]=v
		return self
	def reset(self):
		attributes = [k for k in self.__dict__ if not k.endswith('_fun')]
		for attr in attributes:
			del self.__dict__[attr]

