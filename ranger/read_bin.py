from time import time
import struct
t0=time()
total = 0
with open('test_1m.bin','rb') as f:
	while True:
		raw = f.read(20*8)
		if not raw: break
		rec = struct.unpack('q'*20,raw)
		for x in rec:
			total += x
print(total)
print(time()-t0)
