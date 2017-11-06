import socket
import marshal
import os
from ko_x2 import KO,KV

db = KV('kv-sock','c')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1',9977))
s.listen(100)
while True: # 450k/s
	conn,addr = s.accept()
	#print('incoming',addr)
	fd = conn.fileno()
	f = os.fdopen(fd)
	while True:
		try:
			msg = marshal.load(f)
		except EOFError:
			break
		except Exception as ex:
			print(ex)
			break
		cmd,args = msg[0],msg[1:]
		#print('MSG',cmd,args)
		fun = getattr(db,cmd)
		resp = fun(*args) if args else fun()
		if type(resp) != list:
			resp = 'OK'
		#print('RESP',type(resp),resp)
		marshal.dump(resp,f,2)
	f.close()
	conn.close()
	#print(resp)
s.close()
