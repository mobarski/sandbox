"""Ultra light data frames.
"""

def frame_from_iter(iterable, names):
	"""Create data frame from records.
	"""
	frame = {name:[] for name in names}
	for rec in iterable:
		for i,name in enumerate(names):
			frame[name].append(rec[i])
	return frame

def filter_frame(frame, predicates, select=None):
	"""Filter frame using given predicates.
	"""
	f = {}
	columns = select or frame.keys()
	for col in columns:
		f[col] = [v for p,v in zip(predicates,frame[col]) if p]
	return f

def where(frame,cols,fun):
	"""Calculate predicates
	"""
	predicates = []
	frame_cols = [frame[col] for col in cols]
	for args in zip(*frame_cols):
		predicates.append(1 if fun(*args)  else 0)
	return predicates
