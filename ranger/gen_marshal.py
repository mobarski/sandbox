import marshal
fo = open('test_1m.marshal','wb')
for i in range(1000000):
	rec = []
	for j in range(20):
		rec += [i*20+j]
	marshal.dump(rec,fo)
