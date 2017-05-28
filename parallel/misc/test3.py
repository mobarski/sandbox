import multiprocessing as mp
import subprocess as sp
import sys
import os
import io
import msvcrt

# pass file handle

def wri(fh):
	fd = msvcrt.open_osfhandle(fh,0)
	print(fd,fh)
	if 0:
		f=os.fdopen(fd,'wb')
		f.write('to\n')
		f.write('jest\n')
		f.write('test\n')
		f.flush()
	os.write(fd,b'to\n')
	os.write(fd,b'jest\n')
	os.write(fd,b'test\n')
	os.fsync(fd)
	os.close(fd)

if __name__=="__main__":
	rd,wd = os.pipe()
	#os.write(wd,b'xxx')
	#print(os.read(rd,3))
	wh = msvcrt.get_osfhandle(wd)
	print(wd,wh)
	p = mp.Process(target=wri,args=[wh])
	#rf = os.fdopen(rd,'rb')
	p.start()
	p.join()
	#os.write(wd,b'xxx')
	#os.write(wd,b'yyy')
	#print(os.read(rd,5))
	#print(os.read(rd,5))
	#os.fsync(wd)
	#os.close(wd)
	rh = msvcrt.get_osfhandle(rd)
	print(rd,rh)
	rd2 = msvcrt.open_osfhandle(rh,0)
	print(os.read(rd2,1))
	#print(rf.read())
