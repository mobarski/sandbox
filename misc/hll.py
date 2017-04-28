#https://www.periscopedata.com/blog/hyperloglog-in-pure-sql.html
#http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf

from binascii import crc32
from math import log2

def h(x):
	return crc32(x.encode()) & (1<<31)-1

def msb(x):
	return 31 - int(log2(h(x)))

class hll:
	def __init__(self,buckets=2048):
		self.cnt = [0]*buckets
		self.msb = [0]*buckets
		self.buckets = buckets
	def add(self,x):
		b = h(x) % self.buckets
		self.cnt[b] += 1
		self.msb[b] = max(msb(x),self.msb[b])
	def estimate(self):
		m = self.buckets
		alpha = 0.72134 / (1+1.079/m) # for m>=128
		nominator = alpha * m*m
		denominator = sum([2**(-x) for x in self.msb])
		raw_estimate = nominator / denominator
		all_cnt = sum(self.cnt)
		empty_cnt = sum([1 for x in self.cnt if not x])
		if raw_estimate <= 2.5*m:
			estimate = alpha * m*log2(m/empty_cnt) if empty_cnt else raw_estimate
		elif raw_estimate > 2**32/30:
			estimate = -2**32*log2(1-estimate/2**32)
		else:
			estimate = raw_estimate
		#return int(estimate)
		return min(int(estimate), all_cnt)

ranges = [(0,10000),(0,10000),(0,10000)]

hx = hll(2048)
for lo,cnt in ranges:
	for x in range(lo,lo+cnt):
		hx.add(str(x)*100)
print(hx.estimate())
