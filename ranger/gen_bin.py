import struct
fo = open('test_1m.bin','wb')
for i in range(1000000):
	rec = []
	for j in range(20):
		rec += [i*20+j]
	raw = struct.pack("q"*20,*rec)
	fo.write(raw)
