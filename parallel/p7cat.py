## p7cat.py - parallel concatenation
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: x1

from __future__ import print_function
import sys
import os
from multiprocessing import Process
from time import time

def write_part(path_in, path_out, offset, blocksize=4096):
	fi = open(path_in,'rb')
	fo = open(path_out,'r+b')
	fo.seek(offset)
	while True:
		block = fi.read(blocksize)
		fo.write(block)
		if len(block)<blocksize: break
	fi.close()
	fo.close()

if __name__ == "__main__":
	t0 = time()
	outpath = sys.argv[1]
	filenames = sys.argv[2:]
	print('OUT',outpath)
	print('IN',filenames)

	meta = {} # filename -> size, offset
	offset = 0
	for path in filenames:
		size = os.path.getsize(path)
		meta[path] = (size,offset)
		offset += size

	# allocate disk space
	out = open(outpath,'wb')
	out.seek(offset-1)
	out.write(b'\x00')
	out.close()

	proc = {}
	for path in filenames:
		size,offset = meta[path]
		proc[path] = Process(target=write_part, args=(path, outpath, offset))

	for path in filenames:
		proc[path].start()

	for path in filenames:
		proc[path].join()

	print(time()-t0)
