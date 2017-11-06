N=200000

import socket
from time import time
import marshal

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',9977))
t0=time()
for i in range(N): # 450k/s
	msg = ('__setitem__','k'+str(i),'v'+str(i))
	s.sendall(marshal.dumps(msg,2))
msg = ('sync',)
s.sendall(marshal.dumps(msg,2))
print(N/(time()-t0))
