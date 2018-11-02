import marshal
import os

class disk_cache:
	def __init__(self, dir):
		self.dir = dir
	
	def use(self, key, fun, *args, **kwargs):
		h = '' # TODO
		path = os.path.join(self.dir,key+h+'.marshal')
		if os.path.exists(path):
			obj = marshal.load(open(path,'rb'))
		else:
			obj = fun(*args,**kwargs)
			marshal.dump(obj, open(path,'wb'))
		return obj
