#from cPickle import dump,load
from marshal import dump,load,dumps,loads
from multiprocessing import Lock
import os

from time import time

class no_lock:
	def __enter__(self): pass
	def __exit__(self,*a,**kw): pass

class KO:
	"KV database where keys are in memory and values are stored in separate file"
	def __init__(self,name,lock=None):
		self.name = name
		if os.path.exists(name+'.k'):
			with open(name+'.k','rb') as kf:
				self.offset = load(kf)
		else:
			self.offset = {}
		if not os.path.exists(name+'.v'):
			open(name+'.v','w').close()
		self.wf = open(name+'.v','ab')
		self.wf.seek(0,2)
		self.dirty = True
		self.reopen_if_dirty()
		self.lock = lock or Lock()
		#self.lock = no_lock()

	def reopen_if_dirty(self):
		#self.rf = os.fdopen(os.dup(self.wf.fileno()),'rb')
		if self.dirty:
			self.wf.flush()
			self.rf = open(self.name+'.v','rb')
		self.dirty = False

	### WRITE ###
	
	def set(self,k,v):
		#with self.lock:			
		f = self.wf
		self.offset[k] = f.tell()
		dump(v,f,2)
		self.dirty = True

	def __setitem__(self,k,v):
		self.set(k,v)

	def __delitem__(self,k):
		#with self.lock:
		if k in self.offset: del self.offset[k]
		self.dirty = True

	## def update(self,k,items):
		## self.data.update(items)
	
	def incr(self,k,v=1): # 100k/s
		#with self.lock:
		if k not in self.offset:
			self.set(k,v)
		else:
			curr_val = self.get(k)
			curr_len = self.wf.tell()-self.offset[k]
			new_val = dumps(curr_val + v,2)
			new_len = len(new_val)
			if new_len>curr_len:
				self.set(k,curr_val+v)
			else:
				self.wf.seek(self.offset[k])
				self.wf.write(new_val)
				self.wf.seek(0,2)
				self.dirty = True

	def incr_items(self,items):
		try:
			kv = items.items()
		except:
			kv = items
		for k,v in kv:
			self.incr(k,v)

	### READ ###

	def get(self,k,default=None):
		if k not in self.offset: return default
		self.reopen_if_dirty()
		f = self.rf
		f.seek(self.offset[k])
		return load(f)
	
	def __getitem__(self,k):
		return self.get(k)

	def __contains__(self,k):
		return k in self.offset

	def __len__(self):
		return len(self.offset)

	def items(self):
		for k in self.offset:
			yield k,self.get(k)

	def keys(self):
		return self.offset.keys()
	
	def values(self):
		for k in self.offset:
			yield self.get(k)

	### OTHER ###

	def sync(self):
		with open(self.name+'.k','wb') as kf:
			dump(self.offset,kf,2)
		#import pdb; pdb.set_trace()
		self.reopen_if_dirty()


M = 100
N = 1000*M
db = KO('ko_x2')

t0=time()
if 1:
	for i in range(N):
		db[i] = i
	db.sync()
	## for k in range(M):
		## for i in range(N):
			## db.incr(i,1.2)
	## db.sync()
if 1:
	for i in range(N):
		db[i]
print(N/(time()-t0))
