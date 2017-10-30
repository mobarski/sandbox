import socket
import marshal
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1',8899))
s.listen(1)
while True:
	conn,addr = s.accept()
	print('incoming',addr)
	fd = conn.fileno()
	f = os.fdopen(fd)
	while True:
		try:
			data = marshal.load(f)
		except EOFError:
			break
	f.close()
	conn.close()
	print(data)
