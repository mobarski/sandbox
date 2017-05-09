
import re
class model8(object):
	def __getattribute__(self,x):
		if x.startswith('__') or x in ['update']:
			return object.__getattribute__(self,x)
		v = self.__dict__[x]
		if isinstance(v,str):
			lambda_body = re.sub('{([^}]+)}','self.\\1',v)
			v_str = "(lambda self:%s)(self)" % (lambda_body)
			v = eval(v_str)
		return v
	def update(self,other):
		self.__dict__.update(other.__dict__)
		return self

if __name__=="__main__":
	def zzz(z):
		return z+1
	G = 123
	x = model8()
	x.a = 1
	print(x.a)
	x.b = '{a}+1'
	print(x.b)
	x.c = '{b}*2+{b}/2+G'
	print(x.c)
	y=model8().update(x)
	y.y='{c}/2-zzz({c})'
	print(y.y)
