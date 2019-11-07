from common2 import *
import v8
from rsm import scores,learn_positive,learn_negative
import numpy as np

class rsmc(v8.rsm):
	def __init__(self,n,**kw):
		self.cfg = {'n':n}
		self.cfg.update(kw)
		self.defaults()
		# NEW
		self.cnt = {j:Counter() for j in range(n)}
		self.ctx = deque(maxlen=self.cfg['c']) # context queue
		# OLD
		N = self.cfg['n']
		M = self.cfg['m']
		V = self.cfg['v']
		self.mem = np.zeros((N,M),dtype=np.int32)
		self.neg = np.zeros((N,V),dtype=np.int32)
		self.hit = np.zeros((N,M),dtype=np.int32)
		self.out  = np.zeros(N,dtype=np.int32)
		self.used = np.zeros(N,dtype=np.int32)
	
	def scores(self,input,learning=False):
		mem = self.mem
		out = self.out
		hit = self.hit
		dropout = self.cfg['dropout']
		s = scores(mem,input,out,hit,dropout)
	
	def learn(self,input,y=1):
		self.ctx.clear()
		a_w = self.cfg['awidth']
		a_o = self.cfg['astep']
		input_array = np.array(input, dtype=np.int32)
		for i in range(0,len(input),a_o):
			self.learn_part(input_array[i:i+a_w],y)
	
	def learn_part(self,input,y=1):
		mem = self.mem
		neg = self.neg
		out = self.out
		hit = self.hit
		used = self.used
		dropout = self.cfg['dropout']
		
		if y:
			learn_positive(mem,neg,input,out,used,hit,dropout=0.0,k=4)
		else:
			learn_negative(mem,neg,input,out,used,hit,dropout=0.0,k=4)

# ------------------------------------------------------------------------------
	

if __name__=="__main__":
	nn = rsmc(5,m=5,v=5,k=2,boost=1)
	nn.learn([1,3,4,5],y=1)
	nn.learn([1,5,7,9],y=0)
	nn.learn([1,3,4,9],y=1)
	print(nn.mem)
	print(nn.neg)
	print(nn.hit)
	print(nn.transform_one_v3(np.array([1,3,4,5,7,9],dtype=np.int32)))
