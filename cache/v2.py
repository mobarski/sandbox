import marshal
import sys
import os

class Cache:

	def __init__(self, root_dir):
		self.root = root_dir
		self.dump = marshal.dump
		self.load = marshal.load
	
	# ---[ key1, key2, value interface ]----------------------------------------
	
	def get(self, k1, k2, default=None):	
		path = _path(self.root, k1, k2)
		try:
			with open(path,'rb') as f:
				return self.load(f)
		except:
			return default

	def set(self, k1, k2, value):
		path = _path(self.root, k1, k2)
		if value is not None:
			f = open(path, 'wb')
			self.dump(value, f)
		else:
			if os.path.exists(path):
				os.remove(path)
				#print('xxx set/remove',k1,k2)

	def keys(self, k1=None):
		if k1:
			path = _path(self.root, k1, '')
			return os.listdir(path)
		else:
			return os.listdir(self.root)

	# --------------------------------------------------------------------------

	def top_keys(self, k1, k2_from, k2_to, inclusive=True):
		all = self.keys(k1)
		in_range = _limit_range(all, k2_from, k2_to, inclusive)
		top = _limit_top(in_range)
		return top
	
	def top(self, k1, k2_from, k2_to, inclusive=True):
		top_keys = self.top_keys(k1, k2_from, k2_to, inclusive)
		data = [self.get(k1,k) for k in top_keys]
		return data, top_keys

	def invalid(self, k1, k2, inclusive=False):
		out = []
		k2_list = self.keys(k1)
		for k in k2_list:
			if k2.startswith(k):
				if k2 != k or inclusive:
					out.append(k)
		return out

	def hint_optimize(self): pass # TODO
		

# HELPERS: KEY-VALUE

def _path(root, k1, k2):
	"join path and create directory root/k1 if not exists"
	dir = os.path.join(root,k1)
	if not os.path.exists(dir):
		os.makedirs(dir)
	path = os.path.join(dir,k2)
	return path

# HELPERS: RANGE

def _limit_range(all, k_from, k_to=None, inclusive=True):
	""
	if k_to:
		if inclusive:
			out = [k for k in all if k>=k_from and (k<k_to or k.startswith(k_to))]
		else:
			out = [k for k in all if k>=k_from and k<k_to]
	else:
		# TODO k_from is not string (list / tuple / set)
		out = [k for k in all if k.startswith(k_from)]
	out.sort()
	return out

def _limit_top(k_list):
	""
	if not k_list: return []
	curr = k_list[0]
	out = [curr]
	for k in k_list[1:]:
		if k.startswith(curr):
			pass
		else:
			out += [k]
			curr = k
	return out

def _agg(all, top):
	pass

# ---[ PROCESSING ]-------------------------------------------------------------



# ------------------------------------------------------------------------------

if __name__=="__main__":
	c = Cache('test_dir')
	c.set('k1','k2',None)
	c.set('k1','k21',[1])
	c.set('k1','k22',[2])
	c.set('k1','k23',[3])
	c.set('k1','k3',[3,4,5])
	c.set('k1','k34',[3,4])
	c.set('k1','k35',[3,5])
	c.set('k1','k4',[4,5,6])
	c.set('k1','k',[1,2,3,4,5,6])
	v = c.get('k1','k3')
	print(v)
	all = c.keys('k1')
	print('list_all:k1',all)
	print('list_all',c.keys())
	r = _limit_range(all,'k1','k4',inclusive=True)
	print('range',r)
	print('top',_limit_top(r))
	print('top',c.top('k1','k2','k4'))
	c.invalid('k1','k35',True)
	