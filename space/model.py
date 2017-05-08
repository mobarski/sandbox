class model:
	## core ##############################################
	def __getattr__(self,x):
		d = self.__dict__
		v = d[x] if x in d else d[x+'_fun']
		return v(self) if callable(v) else v
	## aux ##############################################
	def update(self,other):
		for k,v in other.__dict__.items():
			self.__dict__[k]=v
		return self
	def reset(self):
		attributes = [k for k in self.__dict__ if not k.endswith('_fun')]
		for a in attributes:
			del self.__dict__[a]
