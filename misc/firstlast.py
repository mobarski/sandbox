class int_obj(int): pass
def indexed(iterable):
	for i,x in enumerate(iterable):
		idx = int_obj(i)
		idx.first = i==0
		idx.last = i+1==len(iterable)
		yield idx,x

if __name__=="__main__":
	for i,x in indexed("abcdef"):
		print(i,i.first,i.last,x)

