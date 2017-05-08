import re
class model(object):
	def __getattribute__(self,x):
		if x.startswith('__') or x in ('chain',):
			return object.__getattribute__(self,x)
		v = self.__dict__[x]
		if isinstance(v,str):
			lambda_body = re.sub('{([^}]+)}','m.\\1',v)
			v_str = "(lambda m:%s)(self)"%(lambda_body)
			return eval(v_str)
		else:
			return v
	def chain(self,other):
		self.__dict__.update(other.__dict__)
		return self

if 1:
	x = model()
	x.a = 1
	print(x.a)
	x.b = '{a}+1'
	print(x.b)
	x.c = '{b}*2'
	print(x.c)