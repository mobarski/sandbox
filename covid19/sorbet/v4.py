from pickle import dump,load

# TODO doc strings
# TODO index as mem-mapped file - next major version

class sorbet:
	"frozen sequence storage engine"
	
	def __init__(self, path):
		self.path = path
	
	def new(self):
		self.f = open(f"{self.path}.data",'wb')
		self.index = []
		return self
	
	def save(self):
		dump(self.index, open(f"{self.path}.index",'wb'))
		self.f.close()
		self.f = open(f"{self.path}.data",'rb')
		return self
	
	def load(self):
		self.f = open(f"{self.path}.data",'rb')
		self.index = load(open(f"{self.path}.index",'rb'))
		return self
	
	def dump(self, data):
		f = open(f"{self.path}.data",'wb')
		index = []
		for val in data:
			index.append( f.tell() )
			dump(val, f)
		f.close()
		dump(index, open(f"{self.path}.index",'wb'))
		self.index = index
		self.f = open(f"{self.path}.data",'rb')
		return self
	
	def append(self, val):
		self.index.append( self.f.tell() )
		dump(val, self.f)
	
	def __getitem__(self, key):
		if type(key) is slice:
			return self.__getslice__(key)
		else:
			pos = self.index[key]
			self.f.seek(pos)
			return load(self.f)
	
	def __getslice__(self, key):
		start,stop,step = key.indices(len(self))
		for i in range(start,stop,step):
			yield self[i]
	
	def __len__(self):
		return len(self.index)

# ---[ TEST ]-------------------------------------------------------------------

if __name__=="__main__":
	from time import time
	import sys
	label = sys.argv[0][:-3]
	path = f'data/{label}'
	N = 100000
	if 1:
		data = ({'a':i,'aa':i*10} for i in range(N))
		t0=time()
		db = sorbet(path).dump(data)
		print("write time:",f"{time()-t0:.02f}s",f'{N/(time()-t0):.0f} items/s')
	if 1:
		db = sorbet(path).load()
		t0=time()
		for i in range(N):
			db[i]
		print("read time:",f"{time()-t0:.02f}s",f'{N/(time()-t0):.0f} items/s')
	print(list(db[:3]))
	for x in list(db[:3]):
		print(x)
	print(db[10])
