import multiprocessing as mp
import subprocess as sp
import sys
import os
import io

# pass file object

def wri(f):
	#f=os.fdopen(fd,'wb')
	f.write('to\n')
	f.write('jest\n')
	f.write('test\n')
	f.flush()

if __name__=="__main__":
	rd,wd = os.pipe()
	p = mp.Process(target=wri,args=[wd])
	rf=os.fdopen(rd,'rb')
	p.start()
	p.join()
	os.fsync(wd)
	os.close(wd)
	#print(os.read(rd,100))
	print(rf.read())	