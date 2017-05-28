import multiprocessing as mp
import subprocess as sp
import sys
import os
import io
import shlex
import msvcrt

fi=open('test.txt','rb')
fo=sys.stderr
fe=sys.stderr
fo2=open('usunmnie.txt','wb')
fd = fo2.fileno()
fh = msvcrt.get_osfhandle(fd)
print(fd,fh)

#args=['python','upper.py',str(fd)]
args=['python','upper2.py',str(fh)]
p=sp.Popen(args,stdin=fi,stdout=fo,stderr=fe,close_fds=False)
p.wait()
