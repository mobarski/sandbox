from __future__ import print_function
import numpy as np

from random import randint
from heapq import nlargest
from time import time
import marshal

from spatial import random_sdr

# REFERENCES:
## https://numenta.org/resources/HTM_CorticalLearningAlgorithms.pdf

class temporal_pooler:
	def __init__(self,n,k,c,t=100,p_hi=130):
		"""
		Parameters:
		-----------
			n -- number of columns (:int)
			k -- number of columns to fire (:int)
			c -- number of cells per column (:int)
		"""
		self.cfg = {}
		self.cfg['n'] = n
		self.cfg['c'] = c
		self.cfg['k'] = k
		self.cfg['t'] = t
		self.cfg['p_hi'] = p_hi
	
		self.perm = None
		self.conn = None
		self.init()
	
	def init(self):
		c = self.cfg['c']
		n = self.cfg['n']
		k = self.cfg['k']
		t = self.cfg['t']
		p_hi = self.cfg['p_hi']
		
		tx = []
		tx.append(time())
		
		# flat coordinates, use divmod(x,c) to recover column and cell coords
		self.conn = {i:random_sdr(c*n,k) for i in range(c*n)}
		tx.append(time())
		
		self.perm = {(i,j):r for i in range(c*n) for j,r in zip(self.conn[i],np.random.randint(t, p_hi, k))} # 64->0.7s 128->12s
		#self.perm = {i:{j:r for j,r in zip(self.conn[i],np.random.randint(t, p_hi, k))} for i in range(c*n)} # 64->0.26s
		tx.append(time())
		
		for label,t1,t0 in zip(['init conn','init perm'],tx[1:],tx):
			print("{:.3f}\t{}".format(t1-t0,label))

if __name__=="__main__":
	N = 64*64
	K = N*2//100
	C = 4
	tp = temporal_pooler(N,K,C)
	print(len(tp.perm))
	print(len(marshal.dumps(tp.perm,2)))
	exit()
	for i in tp.conn:
		for j in tp.conn[i]:
			jn,jc = divmod(j,C)
			print(i,j,jn,jc)

