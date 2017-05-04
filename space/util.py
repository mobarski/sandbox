class namespace(str): pass

class model(dict):
	def __getattr__(self,x):
		getter = 'get_'+x
		if getter in self.__dict__:
			return self.__dict__[getter]()
		else:
			return self[x]

def to_seconds(h=0,m=0,s=0):
	return h*3600+m*60+s


if __name__=="__main__":
	if 0:
		m=model(a=1,b=2)
		m.get_x = lambda:m.a+m.b
		print(m.a,m.b,m.x)	
	