from const import *

## EX1 ########################

class formula:
	def __init__(self,expr,units):
		self.expr=expr
		self.units=units
	def expand(self):
		return self.expr.format(**self.__dict__)
	def explain(self):
		return self.expr.replace('{','').replace('}','')
	def solve(self):
		return eval(self.expand())
	def copy(self):
		f = formula(self.expr,self.units)
		f.__dict__=self.__dict__.copy()
		return f

if __name__=="__main__":
	v_circ=formula('( ({u}) / ({r}) )**0.5','m/s')
	v_circ.u='GM.sun'
	v_circ.r='D.earth + 400e3'
	print(v_circ.explain())
	print(v_circ.expand())
	print(v_circ.solve())

