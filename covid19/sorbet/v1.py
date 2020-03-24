from pickle import dump,load

# TODO index as mem-mapped file

class DB:
	"append-only sequence storage engine"
	
	def __init__(self, path, mode='r'):
		self.path = path
		self.f = open(f"{path}.data",'wb' if mode=='w' else 'rb')
		self.index = [] if mode=='w' else load(open(f"{path}.index",'rb'))
	
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
	
	def append(self, val):
		self.index.append( self.f.tell() )
		dump(val, self.f)
	
	def extend(self, val_list):
		for val in val_list:
			self.index.append( self.f.tell() )
			dump(val, self.f)

	def close(self):
		self.f.close()
		dump(self.index, open(f"{self.path}.index",'wb'))
	
	def freeze(self):
		self.close()
		self.f = open(f"{path}.data",'rb')


if __name__=="__main__":
	from time import time
	import sys
	label = sys.argv[0][:-3]
	path = f'data/{label}'
	N = 100000
	if 1:
		db = DB(path,'w')
		t0=time()
		for i in range(N):
			db.append({'a':i,'aa':i*10})
		print("write time:",f"{time()-t0:.02f}s",f'{N/(time()-t0):.0f} items/s')
		db.close()
	if 1:
		db = DB(path)
		t0=time()
		for i in range(N):
			db[i]
		print("read time:",f"{time()-t0:.02f}s",f'{N/(time()-t0):.0f} items/s')
	print(list(db[:3]))
	for x in list(db[:3]):
		print(x)
	print(db[10])
