import re

def get_raw_frame(path, encoding='utf8', sep='\t', partition=None, n_col=None):
	if n_col==None:
		with open(path,'rb') as f:
			line = next(f)
			n_col = len(line.split(sep))

	by_col = [[] for _ in range(n_col)]
	with open(path,'rb') as f:
		for line in f:
			rec = line.split(sep)
			for i in range(n_col):
				by_col[i].append(rec[i])
	return by_col

def raw_iter(path, encoding='utf8', sep='\t', partition=None):
	with open(path,'rb') as f:
		for line in f:
			rec = line.split(sep)
			yield rec

def get_frame(input):
	rec = next(input)
	n_col = len(rec)
	by_col = [[v] for v in rec]
	for rec in input:
		for i in range(n_col):
			by_col[i].append(rec[i])
	return by_col

if 1:
	from time import time
	t0=time()
	f = get_raw_frame('__all__.txt',n_col=3)
	#f = get_frame(raw_iter('__all__.txt'))
	print(time()-t0)
	print(len(f))
	print(f[0][0])
	print(f[1][0])
	print(f[2][0])
