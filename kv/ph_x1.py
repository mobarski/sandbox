from UserList import UserList
from heapq import *
from time import time
from random import shuffle
from copy import copy 

class PH(UserList):
	"Persistent Heap"
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
		d = copy(self.data)
		for i in range(n):
			yield heappop(d)

N=1000000
data1 = range(N)
data2 = range(N)
shuffle(data1)
shuffle(data2)
print(data1[:5])
print(data2[:5])

ph = PH(data1)
ph.heapify()
t0=time()
if 0:
	for x in data2:
		ph.add(x)
if 0:
	ph.extend(data2)
	ph.heapify()
if 0:
	ph.top(1000)
print(N/(time()-t0))
