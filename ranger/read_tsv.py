from time import time
t0=time()
f = open('test_100k.tsv')
total = 0
for line in f:
	rec = line.split('\t')
	rec[-1] = rec[-1].rstrip()
	rec = list(map(int,rec))
	for x in rec:
		total += x
print(total)
print(time()-t0)
