from UserList import UserList
from bisect import *
from time import time
from random import shuffle

class PL(UserList):
	"Persistent List"
	def push(self, x):
		insort_left(self.data, x)

N1 = 300000
N = 100000
data1 = range(N1)
data2 = range(N)
shuffle(data1)
shuffle(data2)
pl = PL(data1)
t0=time()
for x in data2:
	pl.push(x)
print(N/(time()-t0))
