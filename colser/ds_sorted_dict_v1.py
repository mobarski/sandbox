
# TODO - bisect operations

class SortedDict:
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
	
	def items(self,a=None,b=None,c=None):
		self.sort()
		if a!=None or b!=None or c!=None:
			return iter(self._items[a:b:c])
		else:
			return iter(self._items)
	
	def keys(self,a=None,b=None,c=None):
		self.sort()
		if a!=None or b!=None or c!=None:
			return (x[0] for x in self._items[a:b:c])
		else:
			return (x[0] for x in self._items)

	def values(self,a=None,b=None,c=None):
		self.sort()
		if a!=None or b!=None or c!=None:
			return (x[1] for x in self._items[a:b:c])
		else:
			return (x[1] for x in self._items)
		
	def update(self,*a,**kw):
		self._items = []
		self.dict.update(*a,**kw)
	
	# -- SINGLE OPERATIONS ---
	
	def sd_set(self,k,v)
		self[k] = v
	
	def sd_get(self,k)
		return self.get(k)
	
	def sd_add(self,k,v):
		try:
			self[k] += v
		except KeyError:
			self[k] = v
		return self[k]
	
	
if __name__=="__main__":
	d = SortedDict(a=3,b=1,c=2,d=(2,2))
	d['x'] = 1.5
	d.sd_add('a',0.1)
	d.sd_add('y',0.1)
	print(list(d.items()))
	print(list(d.items(None,None,2)))

