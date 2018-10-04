fo = open('test_1m.tsv','w')
for i in range(1000000):
	rec = []
	for j in range(20):
		rec += [str(i*20+j)]
	fo.write('\t'.join(rec)+'\n')
