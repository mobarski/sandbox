import multiprocessing as mp
import subprocess as sp
import sys
import os
import io

# pass file descriptor

def wri(fd):
	print('xxx')
	os.write(fd,'to\n')
	os.write(fd,'jest\n')
	os.write(fd,'test\n')
	os.fsync(fd)
	os.close(fd)

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