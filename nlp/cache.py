import marshal
import os

class disk_cache:
	def __init__(self, dir, prefix=''):
		self.dir = dir
		self.prefix = prefix + '_' if prefix else ''
	
	def use(self, key, fun, *args, **kwargs):
		h = '' # TODO
		fn = self.prefix + key + h + '.marshal'
		path = os.path.join(self.dir,fn)
		if os.path.exists(path):
			obj = marshal.load(open(path,'rb'))
		else:
			obj = fun(*args,**kwargs)
			marshal.dump(obj, open(path,'wb'))
		return obj
