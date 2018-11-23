from array import array
from random import randint,shuffle
import numpy as np

def random_sdr(n,w):
	all = list(range(n))
	shuffle(all)
	return set(all[:w])

class spatial_pooler:
	def __init__(self,n,w):
		self.cfg = {}
		self.cfg['n'] = n
		self.cfg['w'] = w # TODO int vs float
		self.conn = {x:random_sdr(n,w) for x in range(n)}
		#self.perm = np.zeros((n,n),dtype=np.uint8)
	def score(self,input):
		conn = self.conn
		score = {x:len(input&conn[x]) for x in conn}
		return score

a = random_sdr(16,8)
b = random_sdr(16,8)
print(a)
print(b)
print(a&b)
print(a|b)
print(a^b)

sp = spatial_pooler(16,4)
print(sp.conn)
print(sp.score(a))
