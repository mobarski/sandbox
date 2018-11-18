"""Disk caching mechanism focused on simplicity and controllability
"""

import marshal
import os
from time import time


# TODO rename missed -> complete? clean? recent?
# TODO refactor

class disk_cache:
	"""simple key-value database for fast caching of basic types
	"""
	def __init__(self, dir, verbose=False, skip=False, reset=False, linear=False):
		self.dir = dir
		if not os.path.exists(dir):
			os.makedirs(dir)
		self.verbose = verbose
		self.skip_cache = skip
		self.reset_cache = reset
		self.missed = False
		self.linear = linear # dont use cached data after first miss/set
		self.ext = ".marshal"
		self.protocol = 2
	
	def use(self, key, fun, *args, **kwargs):
		"""Get the result from cache if possible or call the function and store the result
		"""
		if self.reset_cache:
			return self.set(key, fun, *args, **kwargs)
		if self.skip_cache:
			return self.skip(key, fun, *args, **kwargs)
		if self.linear and self.missed:
			return self.set(key, fun, *args, **kwargs)
		
		t0 = time()
		fn = key + self.ext
		path = os.path.join(self.dir,fn)
		if os.path.exists(path):
			return self.get(key)
		else:
			return self.set(key,fun,*args,**kwargs)
	
	def skip(self, key, fun, *args, **kwargs):
		"""Call function without storing the results in cache
		"""
		t0 = time()
		obj = fun(*args,**kwargs)
		if self.verbose:
			print('{} {:.2f} s'.format(key, time()-t0))
		return obj
	
	def set(self, key, fun, *args, **kwargs):
		"""Call function and store the result in cache
		"""
		t0 = time()
		fn = key + self.ext
		path = os.path.join(self.dir,fn)
		if callable(fun):
			obj = fun(*args,**kwargs)
		else:
			obj = fun # TODO document
		with open(path,'wb') as f:
			marshal.dump(obj, f, self.protocol)
			size = f.tell()
		self.missed = True
		if self.verbose:
			mode = ''
			try:
				len_str = str(len(obj))+' items \t'
			except:
				len_str = ''
			print('{}\t{:.2f} s\t{:.1f} MB\t{}{}'.format(key, time()-t0, 1.0*size/2**20, len_str, mode))
		return obj
	
	def get(self, key, default=None):
		t0 = time()
		fn = key + self.ext
		path = os.path.join(self.dir,fn)
		if os.path.exists(path):
			with open(path,'rb') as f:
				obj = marshal.load(f)
				size = f.tell()
			mode = 'from cache'
		else:
			obj = default
			mode = ''
		if self.verbose:
			try:
				len_str = str(len(obj))+' items \t'
			except:
				len_str = ''
			print('{}\t{:.2f} s\t{:.1f} MB\t{}{}'.format(key, time()-t0, 1.0*size/2**20, len_str, mode))
		return obj

	# TODO rename
	def set_map(self, key, obj, columns=None):
		t0 = time()
		path = os.path.join(self.dir, key)
		if not os.path.exists(path):
			os.makedirs(path)
		cols = columns or obj.keys()
		size = 0
		for col in cols:
			p = os.path.join(path, col + self.ext)
			with open(p,'wb') as f:
				marshal.dump(obj[col], f, self.protocol)
				size += f.tell()
		if self.verbose:
			mode = ''
			print('{}\t{:.2f} s\t{:.1f} MB\t{}'.format(key, time()-t0, 1.0*size/2**20, mode))
		return obj
	
	# TODO rename
	def get_map(self, key, columns=None):
		t0 = time()
		obj = {}
		path = os.path.join(self.dir, key)
		cols = columns or [p.replace(self.ext,'') for p in os.listdir(path)]
		size = 0
		for col in cols:
			p = os.path.join(path,col + self.ext)
			with open(p,'rb') as f:
				obj[col] = marshal.load(f)
				size += f.tell()
		if self.verbose:
			mode = ''
			print('{}\t{:.2f} s\t{:.1f} MB\t{}'.format(key, time()-t0, 1.0*size/2**20, mode))
		return obj
	