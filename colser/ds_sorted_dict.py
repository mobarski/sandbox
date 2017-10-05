
# TODO - bisect operations

class SortedDictCore:
	def __init__(self, *a, **kw):
		self._items = []
		self.dict = dict(*a,**kw)

	##

	def __setitem__(self,k,v):
		self._items = []
		self.dict[k]=v
	
	def __getitem__(self,k):
		return self.dict[k]
	
	def __delitem__(self,k):
		self._items = []
		del self.dict[k]
	
	##
	
	def sort(self):
		if self._items: return
		self._items = sorted(self.dict.items(),key=lambda x:(x[1],x[0]))
	
	def items(self):
		self.sort()
		return self._items
	
	def update(self,*a,**kw):
		self._items = []
		self.dict.update(*a,**kw)
	

class SortedDict(SortedDictCore):
	
	def sd_get(self,k):
		return self.dict.get(k)
	
	def sd_set(self,k,v):
		self[k] = v

	def sd_del(self,k):
		if k in self.dict:
			del self.dict[k]

	def sd_add(self,k,v):
		try:
			self[k] += v
		except KeyError:
			self[k] = v
		return self[k]

	def sd_items(self,a=None,b=None,c=None):
		if a is not None or b is not None or c is not None:
			return self.items()
		else:
			return self.items()[a:b:c]

	# *_many

	def sd_get_many(self,k_iter):
		return (self.sd_get(k) for k in k_iter)


	def sd_set_many(self,kv_iter):
		for k,v in kv_iter:
			self.sd_set(k,v)
	
	def sd_del_many(self,k_iter):
		for k in k_iter:
			self.sd_del(k)

	def sd_add_many(self,kv_iter):
		out = []
		for k,v in kv_iter:
			x = self.sd_add(k,v)
			out.append(x)
		return out


if __name__=="__main__":
	d = SortedDict(a=3,b=1,c=2,d=(2,2))
	d['x'] = 1.5
	d.sd_add('a',0.1)
	d.sd_add('y',0.1)
	print(d.items()[-2:])

