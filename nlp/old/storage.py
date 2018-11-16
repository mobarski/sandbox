import marshal
import os

# TODO ??? encode/decode names

class storage:
	def __init__(self, path):
		self.path = path
		if not os.path.exists(path):
			os.makedirs(path)
	
	def set(self, name, val):
		path = os.path.join(self.path, name)
		with open(path,'wb') as f:
			marshal.dump(val,f)
	
	def get(self, name, default=None):
		path = os.path.join(self.path, name)
		if not os.path.exists(path):
			return default
		with open(path,'wb') as f:
			val = marshal.load(f)
		return val
	
	# TODO rename
	def set_map(self, name, obj, columns=None):
		path = os.path.join(self.path, name)
		if not os.path.exists(path):
			os.makedirs(path)
		cols = columns or obj.keys()
		for col in cols:
			p = os.path.join(self.path, name, col)
			with open(p,'wb') as f:
				marshal.dump(obj[col],f)
	
	# TODO rename
	def get_map(self, name, columns=None):
		obj = {}
		cols = columns or os.listdir(os.path.join())
		for col in cols:
			p = os.path.join(self.path,name,col)
			with open(p,'rb') as f:
				obj[col] = marshal.load(f)
		return obj

if __name__=="__main__":
	s = storage('./tmp')
	data = dict(a=[1,2,3,4,5],b=list(range(100)),c=["a","c","b"])
	s.set('test3',data)
	s.set_map('test2',data)
	