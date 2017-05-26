import multiprocessing as mp
import subprocess as sp
import sys
import os
import io

def wri(f):
	#f=os.fdopen(fd,'wb')
	f.write('to\n')
	f.write('jest\n')
	f.write('test\n')
	f.flush()

rd,wd = os.pipe()
wf = io.open(wd,'wb')
p = mp.Process(target=wri,args=[wf])
p.start()
p.join()
wf.close()
#print(os.read(rd,100))
rf=os.fdopen(rd,'rb')
print(rf.read())
