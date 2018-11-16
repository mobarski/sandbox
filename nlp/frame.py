"""Ultra simple data frames.
"""

def frame_from_iter(iterable, names):
	"""Create data frame from records.
	"""
	frame = {name:[] for name in names}
	for rec in iterable:
		for i,name in enumerate(names):
			frame[name].append(rec[i])
	return frame

def iter_from_frame(frame, names):
	"""Iterate through data frame
	"""
	return zip(*[iter(frame[c]) for c in names])

# TODO use columnar.select
def filter_frame(frame, predicates, select=None):
	"""Filter frame using given predicates.
	"""
	f = {}
	columns = select or frame.keys()
	for col in columns:
		f[col] = [v for p,v in zip(predicates,frame[col]) if p]
	return f

# TODO use columnar.select
def where(frame, cols, fun):
	"""Calculate predicates
	"""
	predicates = []
	frame_cols = [frame[col] for col in cols]
	for args in zip(*frame_cols):
		predicates.append(1 if fun(*args)  else 0)
	return predicates

# TODO use columnar.select
def filtered(data,params,fun=None):
	if fun:
		for d,p in zip(data,params):
			if fun(p):
				yield d
	else:
		for d,p in zip(data,params):
			if p:
				yield d		

# TODO multiprocessing and parition operations

if __name__=="__main__":
	def fff(vals):
		out = []
		for x in "abcdefghijklmnop":
			out.append(1 if x in vals else 0)
		return out
	data = [[1,2,3,'abc'],[44,55,66,'def'],[777,888,999,'ghi'],[123,456,789,'jkl']]
	f = frame_from_iter(data,"abcd")
	i = iter_from_frame(f,"cbda")
	print(f)
	print(list(i))
	print
	a = [0,1,2,3,4,5]
	b = [0,1,0,1,0,1]
	c = [1,2,1,2,1,2]
	print(list(filtered(a,b)))
	d = map(lambda x:x==2,c)
	print(list(filtered(a,d)))


