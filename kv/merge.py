from UserDict import UserDict
from time import time
from random import shuffle

## def merge(aa,bb,key=None):
	## "merge (no optimization)" # 300/s
	## out = []
	## ia = 0
	## ib = 0
	## while True:
		## if ia==len(aa):
			## out.extend(bb[ib:])
			## break
		## if ib==len(bb):
			## out.extend(aa[ia:])
			## break

		## if key:
			## va = key(aa[ia])
			## vb = key(bb[ib])
		## else:
			## va = aa[ia] 
			## vb = bb[ib]

		## if va <= vb:
			## out.append(aa[ia])
			## ia += 1
		## else:
			## out.append(bb[ib])
			## ib += 1
	## return out

## def merge(aa,bb,key=None):
	## "optimized merge" # 457/s
	## out = []
	## ia = 0
	## ib = 0
	## len_aa=len(aa)
	## len_bb=len(bb)

	## if len_aa>0: va=key(aa[0]) if key else aa[0]
	## if len_bb>0: vb=key(bb[0]) if key else bb[0]
	## while True:
		## if ia==len_aa:
			## out.extend(bb[ib:])
			## break
		## if ib==len_bb:
			## out.extend(aa[ia:])
			## break

		## try:
			## if va <= vb:
				## out.append(aa[ia])
				## ia += 1
				## va=key(aa[0]) if key else aa[0]
			## else:
				## out.append(bb[ib])
				## ib += 1
				## vb=key(bb[0]) if key else bb[0]
		## except IndexError: pass
	## return out

def merge(aa,bb,key=None):
	"optimized merge x2" # 465k/s
	out = []
	ia = 0
	ib = 0
	len_aa=len(aa)
	len_bb=len(bb)

	if len_aa==0: return bb
	if len_bb==0: return aa

	if len_aa>0: va=key(aa[0]) if key else aa[0]
	if len_bb>0: vb=key(bb[0]) if key else bb[0]
	while True:
		try:
			if va <= vb:
				out.append(aa[ia])
				ia += 1
				va=key(aa[0]) if key else aa[0]
			else:
				out.append(bb[ib])
				ib += 1
				vb=key(bb[0]) if key else bb[0]
		except IndexError:
			if ia==len_aa:
				out.extend(bb[ib:])
				break
			if ib==len_bb:
				out.extend(aa[ia:])
				break
	return out

## def merge(aa,bb,key=None):
	## "optimized merge x3" # 465k/s
	## ia = 0
	## ib = 0
	## len_aa=len(aa)
	## len_bb=len(bb)

	## if len_aa==0:
		## for x in bb:
			## yield x
	## if len_bb==0:
		## for x in aa:
			## yield x

	## if len_aa>0: va=key(aa[0]) if key else aa[0]
	## if len_bb>0: vb=key(bb[0]) if key else bb[0]
	## while True:
		## try:
			## if va <= vb:
				## yield aa[ia]
				## ia += 1
				## va=key(aa[0]) if key else aa[0]
			## else:
				## yield bb[ib]
				## ib += 1
				## vb=key(bb[0]) if key else bb[0]
		## except IndexError:
			## if ia==len_aa:
				## for x in bb[ib:]:
					## yield x
				## break
			## if ib==len_bb:
				## for x in aa[ia:]:
					## yield x
				## break

a = [1,3,5,7,9,11]
b = [0,2,4,6,8]
print(merge(a,b))

a = [(9,1),(7,3),(3,5)]
b = [(1,0),(5,2),(4,4)]
print(merge(a,b,key=lambda x:x[1]))

class OD(UserDict):
	def __init__(self):
		UserDict.__init__(self)
		self.sorted = []
		self.dirty = []
	
	def update(self,d):
		self.data.update(d)
		self.dirty.extend(d)
	
	def sort(self):
		self.dirty.sort(key=lambda k:self.data[k])
		self.sorted = merge(self.sorted, self.dirty, key=lambda k:self.data[k])
		self.dirty = []
	
	def top(self,n):
		for k in self.sorted[:n]:
			yield k,self.data[k]


N = 1000000
v = range(N)
shuffle(v)
data1 = {i:0.1+v[i] for i in range(N)}
data2 = {N+i:0.01+v[i] for i in range(N)}
d = OD()
d.update(data1)
d.sort()
t0=time()
d.update(data2)
d.sort()
x = d.top(6)
print(N/(time()-t0))
print(list(x))

if 1:
	t0=time()
	data1.update(data2)
	list(sorted(data1.items(),key=lambda x:x[1]))
	print(N/(time()-t0))
