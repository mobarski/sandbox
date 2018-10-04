from time import time
import marshal
t0=time()
total = 0
with open('test_1m.marshal','rb') as f:
	while True:
		try:
			rec = marshal.load(f)
		except EOFError: break
		for x in rec:
			total += x
print(total)
print(time()-t0)
