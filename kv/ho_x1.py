#from cPickle import dump,load
from marshal import dump,load,dumps,loads
from multiprocessing import Lock
import os

# TODO - pelna obsluga mode
# TODO - setup/config/meta() do ustawiania kompresji i serde, osobny plik z ustawieniami

from time import time

def as_pairs(items):
	try:
		return items.items()
	except:
		return items

class no_lock:
	def __enter__(self): pass
	def __exit__(self,*a,**kw): pass

def h64(s):
	return hash(s)+hash(s+s)<<32

class HO:
	"KV database where hash(key)->value_offset is in memory and values and keys in separate files"
	def __init__(self,name,mode='c',lock=None):
		self.name = name
		self.mode = mode
		if os.path.exists(name+'.ho') and mode!='n':
			with open(name+'.ho','rb') as hf:
				self.offset = load(hf)
		else:
			self.offset = {}
		if not os.path.exists(name+'.v'):
			open(name+'.v','w').close()
		if not os.path.exists(name+'.k'):
			open(name+'.k','w').close()
		self.wf = open(name+'.v','ab')
		self.wf.seek(0,2)
		self.kf = open(name+'.k','ab')
		self.kf.seek(0,2)
		self.dirty = True
		self.reopen_if_dirty()

	def reopen_if_dirty(self):
		if self.dirty:
			self.wf.flush()
			self.kf.flush()
			self.rf = open(self.name+'.v','rb')
		self.dirty = False

	### WRITE ###
	
	def set(self,k,v):
		h = h64(k)
		f = self.wf
		if h not in self.offset:
			self.kf.write(k+'\n')
		self.offset[h] = f.tell()
		dump(v,f,2)
		self.dirty = True

	def __setitem__(self,k,v):
		self.set(k,v)

	def __delitem__(self,k):
		h = h64(k)
		if h in self.offset: del self.offset[h]
		self.dirty = True

	def update(self,items):
		f = self.wf
		for k,v in as_pairs(items):
			h = h64(k)
			if h not in self.offset:
				self.kf.write(k+'\n')
			self.offset[h] = f.tell()
			dump(v,f,2)
		self.dirty = True
		return self

	def clear(self):
		self.offset.clear()
		open(self.name+'.v','w').close()
		open(self.name+'.k','w').close()
		self.dirty = True
		return self

	### READ ###

	def get(self,k,default=None):
		h = h64(k)
		if h not in self.offset: return default
		self.reopen_if_dirty()
		f = self.rf
		f.seek(self.offset[h])
		return load(f)
	
	def __getitem__(self,k):
		return self.get(k)

	def __contains__(self,k):
		h = h64(k)
		return h in self.offset

	def __len__(self):
		return len(self.offset)

	def items(self):
		for k in self.keys():
			h = h64(k)
			yield k,self.get(k)

	def keys(self):
		f = open(self.name+'.k','r')
		for k in f:
			yield k.rstrip()
	
	def values(self): # TODO optimize
		for k in self.keys():
			yield self.get(k)

	### OTHER ###

	def sync(self):
		with open(self.name+'.ho','wb') as hf:
			dump(self.offset,hf,2)
		#import pdb; pdb.set_trace()
		self.reopen_if_dirty()
		return self

if __name__=="__main__":
	M = 100
	N = 1000*M
	db = HO('data/ho_x1')

	t0=time()
	if 0:
		for i in range(N):
			db[str(i)*5] = i
		db.sync()
		## for k in range(M):
			## for i in range(N):
				## db.incr(i,1.2)
		## db.sync()
	if 0:
		for i in range(N):
			db[str(i)*5]
	if 1:
		from itertools import islice
		print(list(islice(db.items(),100)))
	#print(N/(time()-t0))
