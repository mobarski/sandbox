from random import randint
from time import time

def random_rec(dices):
	out = []
	for n,d in dices:
		total = 0
		for i in range(n):
			total += randint(1,d)
		out += [total]
	return out

if __name__=="__main__":
	t0=time()
	f = open('random.tsv','w')
	f.write('\t'.join(['id','a1','a2','a3','b1','b2','b3','c1','c2','c3','d1','d2','d3']))
	f.write('\n')
	for i in range(100000):
		rec = random_rec([(1,100000),(1,10),(2,10),(3,10),(1,100),(2,100),(3,100),(1,1000),(2,1000),(3,1000),(1,10000),(2,10000),(3,10000)])
		f.write('\t'.join(map(str,rec)))
		f.write('\n')
	print(time()-t0)
	print(1.0*i/(time()-t0))
