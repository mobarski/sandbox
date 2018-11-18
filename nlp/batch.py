from math import ceil

def partitions(n_items, n_parts):
	out = []
	cnt = n_items
	hi = 0
	for i in range(n_parts):
		lo = hi
		hi = int(1.0*cnt/n_parts*(i+1))
		out.append((lo,hi))
	return out

def partitioned(data, n):
	return [data[lo:hi] for lo,hi in partitions(len(data),n)]

if __name__=="__main__":
	x = "abcdefghijk"
	lo_hi = partitions(len(x),1)
	for lo,hi in lo_hi:
		print(lo,hi,x[lo:hi])

