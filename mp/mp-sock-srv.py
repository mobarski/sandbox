import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1',8899))
s.listen(1)
while True:
	conn,addr = s.accept()
	print(conn,addr)
	while True:
		data = conn.recv(16)
		if data:
			pass
		else:
			break
	conn.close()
