def iselect(data, predicates, positive=True):
	if positive:
		return (d for d,p in zip(data,predicates) if p)
	else:
		return (d for d,p in zip(data,predicates) if not p)

def select(data, predicates, positive=True):
	"""select elements from list
	
	Parameters:
	-----------
	
	data : iterable
		data from which the elements will be selected
		
	predicates : iterable
		boolean values that decide which data elements will be selected
		
	positive : boolean, default=False
		whether positive or negative matching elements should be selected
		
	"""
	return list(iselect(data, predicates, positive))


if __name__=="__main__":
	a = [1,2,3,4,5,6,7,8,9]
	b = [1,2,1,2,1,2,3,2,3]
	c = [9,8,7,6,5,4,3,2,1]
	
	z = [x==1 for x in b]
	r = select(a,z)
	print(list(r))

	r = select(a,[x==1 for x in b])
	print(list(r))
	
	p = [x==2 for x in b]
	x1 = select(a,p)
	x2 = select(a,p,False)
	print(x1,x2)

