N=200000

import socket
from time import time
from marshal import dumps

s = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
s.connect('./unix-socket')
t0=time()
for i in range(N):
	s.sendall(dumps(i))
print(N/(time()-t0))
