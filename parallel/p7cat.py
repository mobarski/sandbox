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
	print("\n\tP7 CONCAT START\n")
	outpath = sys.argv[1]
	filenames = sys.argv[2:]
	#print('\tOUT',outpath)
	#print('\tIN\n',filenames)

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
		p = Process(target=write_part, args=(path, outpath, offset))
		p.start()
		print("\tBEGIN  pid:{0}  size:{2}  offset:{1}".format(p.pid,offset,size))
		proc[path] = p
		
	sys.stdout.flush()

	for path in filenames:
		p = proc[path]
		p.join()
		print("\tEND    pid:{0}".format(p.pid))


	print("\n\tRUN_TIME_TOTAL:{0:.1f}s\n".format(time()-t0))
