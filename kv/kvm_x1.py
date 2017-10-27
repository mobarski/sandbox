import marshal

from time import time

class KVM:
	def __init__(self,data=None):
		self.data = data or {}

	### WRITE ###
	
	def set(self,k,v):
		self.data[k] = v

	def __setitem__(self,k,v):
		self.set(k,v)

	def __delitem__(self,k):
		if k in self.data: del self.data[k]

	def update(self,items):
		self.data.update(items)
	
	def incr(self,k,v=1):
		self.data[k] = self.data.get(k,0) + v

	def incr_items(self,items):
		try:
			kv = items.items()
		except:
			kv = items
		for k,v in kv:
			self.incr(k,v)

	### READ ###

	def get(self,k,default=None):
		return self.data.get(k,default)
	
	def __getitem__(self,k):
		return self.get(k)

	def __contains__(self,k):
		return k in self.data

	def __len__(self):
		return len(self.data)

	def items(self):
		return self.data.items()

	def keys(self):
		return self.data.keys()
	
	def values(self):
		return self.data.values()

	### OTHER ###

	def save(self,path):
		f = open(path,'w')
		marshal.dump(self.data,f,2)

	def load(self,path):
		f = open(path,'r')
		self.data = marshal.load(f)


class KVML(KVM):
	def __init__(self,data=None):
		KVM.__init__(self,data)
		self.log = []
	
	def set(self,k,v):
		self.log.append(('set',k,v))
		self.data[k] = v

	def __delitem__(self,k):
		self.log.append(('__delitem__',k))
		if k in self.data: del self.data[k]

	def update(self,k,items):
		self.log.append(('update',k,items))
		self.data.update(items)
	
	def incr(self,k,v=1):
		self.log.append(('incr',k,v))
		self.data[k] = self.data.get(k,0) + v

	def incr_items(self,items):
		self.log.append(('incr_items',k,v))
		try:
			kv = items.items()
		except:
			kv = items
		for k,v in kv:
			self.incr(k,v)
	
	def save(self,path):
		f = open(path,'w')
		marshal.dump(self.log,f,2)

	def load(self,path):
		f = open(path,'r')
		log = marshal.load(f)
		for op in log:
			name,args = op[0],op[1:]
			getattr(self,name)(*args)
			
			

N = 1000000
db = KVML()
t0=time()
if 0:
	for i in range(N):
		db[i] = i
	db.save('kvm_x1.kvm')
	db.data = {}
if 1:
	db.load('kvm_x1.kvm')
print(N/(time()-t0))
