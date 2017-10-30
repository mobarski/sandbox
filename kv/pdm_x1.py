import marshal
from UserDict import UserDict

from time import time

def kv_items(items):
	try:
		return items.items()
	except:
		return items

class PDM(UserDict):
	"Persistant Dictionary for Mixed read/write workloads"
	def __init__(self,data=None):
		UserDict.__init__(self,data)
		self.changed = set()
	
	### READ ###
	
	def __getitem__(self,k):
		return self.get(k)

	### WRITE ###
	
	def set(self,k,v):
		if v is None:
			del self[k]
		else:
			self.data[k] = v
			self.changed.add(k)

	def __setitem__(self,k,v):
		self.set(k,v)

	def __delitem__(self,k):
		if k in self.data:
			del self.data[k]
			self.changed.add(k)

	def update(self,items):
		self.data.update(items)
		for k,v in kv_items(items):
			if v is None:
				del self[k]
		self.changed.update(items)
	
	def incr(self,k,v=1):
		self.data[k] = self.data.get(k,0) + v
		self.changed.add(k)

	def incr_items(self,items): # TODO rename to update_incr, incr_update
		for k,v in kv_items(items):
			self.incr(k,v)
		self.changed.update(items)

	### OTHER ###

	def save(self,path):
		with open(path,'wb') as f:
			marshal.dump(self.data,f,2)
		self.changed.clear()

	def load(self,path):
		with open(path,'rb') as f:
			self.data = marshal.load(f)
		self.changed.clear()
	
	def save_delta(self,path):
		with open(path,'wb') as f:
			marshal.dump({k:self.data.get(k) for k in self.changed},f,2)
		self.changed.clear()

	def load_delta(self,path):
		with open(path,'rb') as f:
			items = marshal.load(f)
			self.data.update(items)
			for k,v in kv_items(items):
				if v is None:
					del self[k]
		self.changed.clear()

N = 1000000
db = KVM()
t0=time()
if 1:
	for i in range(N):
		db[i] = i
	db.save_delta('pdm_x1.pdm')
if 0:
	db.load_delta('pdm_x1.pdm')
print(N/(time()-t0))