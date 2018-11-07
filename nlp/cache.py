"""Disk caching mechanism focused on simplicity and controllability
"""

import marshal
import os
from time import time

# TODO rename missed -> complete? clean? recent?
# TODO refactor
# TODO data_structures (fun=None???)
# TODO h tylko na podstawie kwargs
# TODO h na podstawie args i kwargs

class disk_cache:
	def __init__(self, dir, prefix='', verbose=False, skip=False, reset=False, linear=False):
		self.dir = dir
		self.verbose = verbose
		self.skip_cache = skip
		self.reset_cache = reset
		self.prefix = prefix + '_' if prefix else ''
		self.missed = False
		self.linear = linear # dont use cached data after first miss/set
	
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
		h = '' # TODO
		fn = self.prefix + key + h + '.marshal'
		path = os.path.join(self.dir,fn)
		if os.path.exists(path):
			with open(path,'rb') as f:
				obj = marshal.load(f)
				size = f.tell()
			mode = 'from cache'
		else:
			obj = fun(*args,**kwargs)
			with open(path,'wb') as f:
				marshal.dump(obj, f)
				size = f.tell()
			self.missed = True
			mode = ''
		if self.verbose:
			print('{}\t{:.2f} s\t{:.1f} MB\t{}'.format(key, time()-t0, 1.0*size/2**20, mode))
		return obj
	
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
		h = '' # TODO
		fn = self.prefix + key + h + '.marshal'
		path = os.path.join(self.dir,fn)
		if callable(fun):
			obj = fun(*args,**kwargs)
		else:
			obj = fun # TODO document
		with open(path,'wb') as f:
			marshal.dump(obj, f)
			size = f.tell()
		self.missed = True
		mode = ''
		if self.verbose:
			print('{}\t{:.2f} s\t{:.1f} MB\t{}'.format(key, time()-t0, 1.0*size/2**20, mode))
		return obj
	
	def get(self, key, default=None):
		t0 = time()
		fn = self.prefix + key + '.marshal'
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
			print('{}\t{:.2f} s\t{:.1f} MB\t{}'.format(key, time()-t0, 1.0*size/2**20, mode))
		return obj
