from itertools import islice
import re

def tsv_iter_iter(lines, sep='\t', encoding='utf8',
		line_offset=None, line_limit=None):
	it = iter(lines)
	if line_offset:
		next(islice(it,line_offset,line_offset),None)
	if line_limit:
		it = islice(it,line_limit)
	for line in it:
		line = line.rstrip('\r\n')
		if encoding:
			line = line.decode(encoding)
		rec = line.split(sep)
		yield rec

def tsv_iter(path, sep='\t', encoding='utf8',
		file_offset=None, line_offset=None,
		file_limit=None, line_limit=None):
	with open(path,'rb') as f:
		if file_offset:
			f.seek(file_offset)
		it = tsv_iter_iter(f, sep, encoding, line_offset, line_limit)
		if file_limit:
			for rec in it:
				if f.tell()>=file_limit: break
				yield rec
		else:
			for rec in it:
				yield rec

def tsv_header(path, sep='\t', encoding='utf8'):
	with open(path,'rb') as f:
		line = next(f)
		line = line.rstrip('\r\n')
		if encoding:
			line = line.decode(encoding)
		rec = line.split(sep)
	return rec

# ultra light data frames

def frame_from_iter(iterable, names):
	frame = {name:[] for name in names}
	for rec in iterable:
		for i,name in enumerate(names):
			frame[name].append(rec[i])
	return frame

def filter_frame(frame, predicates, select=None):
	f = {}
	columns = select or frame.keys()
	for col in columns:
		f[col] = [v for p,v in zip(predicates,frame[col]) if p]
	return f

def where(frame,cols,fun):
	predicates = []
	frame_cols = [frame[col] for col in cols]
	for args in zip(*frame_cols):
		predicates.append(1 if fun(*args)  else 0)
	return predicates

