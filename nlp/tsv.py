"""TSV files operations
"""

from itertools import islice
import re

def tsv_iter_iter(lines, sep='\t', encoding='utf8',
		line_offset=None, line_limit=None):
	"""Return record iterator for given line iterator.
	"""
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
	"""Return record iterator for given file.
	"""
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
	"""Return column names for given file.
	"""
	with open(path,'rb') as f:
		line = next(f)
		line = line.rstrip('\r\n')
		if encoding:
			line = line.decode(encoding)
		rec = line.split(sep)
	return rec
