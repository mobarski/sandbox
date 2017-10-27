from time import time
from random import shuffle

class VK:
	def __init__(self,data=None):
		self.kv = {}
		self.k = []
	
	def update(self, d):
		self.kv.update(d)
		self.k.extend(d)
		
	def sort(self):
		kv = self.kv
		self.k.sort(key=lambda x:kv[x])
	
	def top(self, n):
		for k in self.k[:n]:
			yield k,self.kv[k]


class VK2:
	def __init__(self,data=None):
		self.kv = {}
		self.kvl = []
	
	def update(self, d):
		self.kv.update(d)
		self.kvl.extend(d.)
		
	def sort(self):
		self.vk.sort()
	
	def top(self, n):
		for k in self.k[:n]:
			yield k,self.kv[k]


N=100000
v = range(N)
shuffle(v)
data1 = [(i,0.1+v[i]) for i in range(N)]
data2 = [(i,0.2+v[i]) for i in range(N)]
shuffle(data1)
shuffle(data2)
data1 = dict(data1)
data2 = dict(data2)
vk=VK()
vk.update(data1)
t0=time()
vk.sort()
x=list(vk.top(5))
print(N/(time()-t0))
print(x)
