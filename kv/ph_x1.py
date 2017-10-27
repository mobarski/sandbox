from UserList import UserList
from heapq import *
from time import time
from random import shuffle

class PH(UserList):
	def heapify(self):
		heapify(self.data)
	def push(self, x):
		heappush(self.data,x)
	def pop(self):
		heappop(self.data)
	def pushpop(self, x):
		return heappushpop(self.data, x)
	def poppush(self, x):
		return heapreplace(self.data, x)
	def top(self, n):
		pass

N=100000
data1 = range(N)
data2 = range(N)
shuffle(data1)
shuffle(data2)
print(data1[:5])
print(data2[:5])

ph = PH(data1)
t0=time()
#for x in data2:
#	ph.add(x)
ph.extend(data2)
ph.heapify()

print(N/(time()-t0))
