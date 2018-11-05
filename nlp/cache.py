"""Disk caching mechanism focused on simplicity and controllability
"""

import marshal
import os
from time import time

# TODO refactor
# TODO data_structures (fun=None???)
# TODO h tylko na podstawie kwargs
# TODO h na podstawie args i kwargs

class disk_cache:
	def __init__(self, dir, prefix='', show_time=False, skip=False, reset=False, linear=False):
		self.dir = dir
		self.show_time = show_time
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
			obj = marshal.load(open(path,'rb'))
		else:
			obj = fun(*args,**kwargs)
			marshal.dump(obj, open(path,'wb'))
			self.missed = True
		if self.show_time:
			print('{} {:.2f} s'.format(key, time()-t0))
		return obj

	def skip(self, key, fun, *args, **kwargs):
		"""Call function without storing the results in cache
		"""
		t0 = time()
		obj = fun(*args,**kwargs)
		if self.show_time:
			print('{} {:.2f} s'.format(key, time()-t0))
		return obj
	
	def set(self, key, fun, *args, **kwargs):
		"""Call function and store the result in cache
		"""
		t0 = time()
		h = '' # TODO
		fn = self.prefix + key + h + '.marshal'
		path = os.path.join(self.dir,fn)
		obj = fun(*args,**kwargs)
		marshal.dump(obj, open(path,'wb'))
		self.missed = True
		if self.show_time:
			print('{} {:.2f} s'.format(key, time()-t0))
		return obj
	