from v5 import *

def test1():
	X = [random_vector(100,0,1) for i in range(100)]
	X = list(map(rsm.sparsify,X))
	nn = rsm(50,7,13)
	s=nn.score_one(X[0])
	print(sum(s.values()))
	for i in range(2):
		for x in X:
			nn.learn(x,1)
	s=nn.score_one(X[0])
	print(sum(s.values()))
	from pprint import pprint
	pprint(nn.stats())
	pprint(nn.mem)
	pprint(nn.vol)

def test2():
	# data
	X1 = [set(combinations(1000,50)) for i in range(10)]
	X2 = [set(combinations(1000,50)) for i in range(10)]
	X3 = [set(combinations(1000,50)) for i in range(10)]
	# learning
	nn = rsm(10,5)
	for i in range(100):
		if 1: # negative
			for x in X2:
				nn.learn(x,1,negative=True)
		for x in X1: # positive
			nn.learn(x,3,decay=0.0,dropout=0.0,fatigue=0)
			#print(nn.mem)
	# scoring
	m = 6
	s1 = [nn.score_one(x,1,method=m) for x in X1]
	s2 = [nn.score_one(x,1,method=m) for x in X2]
	s3 = [nn.score_one(x,1,method=m) for x in X3]
	if 1:
		print('X1 -> {:.03f} {:.03f} {:.03f}'.format(avg(s1),min(s1),max(s1)))
		print('X2 -> {:.03f} {:.03f} {:.03f}'.format(avg(s2),min(s2),max(s2)))
		print('X3 -> {:.03f} {:.03f} {:.03f}'.format(avg(s3),min(s3),max(s3)))
	if 0:
		print(list(sorted(s1,reverse=True)))
		print(list(sorted(s2,reverse=True)))
	# other
	if 1:
		print(X1)
		print(nn.mem)
		print(nn.win)
		print(nn.tow)
	# stats
	if 0:
		pprint(nn.stats('m'))
	return avg(s1)

def test3():
	X1 = [set(combinations(1000,50)) for i in range(10)]
	X2 = [set(combinations(1000,50)) for i in range(10)]
	Y1 = [1 for x in X1]
	Y2 = [0 for x in X2]
	# learning
	nn = rsm(10,5)
	for i in range(2):
		if 1: # negative
			for x in X2:
				nn.learn(x,1,negative=True)
		for x in X1: # positive
			nn.learn(x,1,decay=0.0,dropout=0.0,fatigue=0)
	# score
	for kind in ['f1','acc','prec','sens','spec']:
		s = nn.score(X1+X2,Y1+Y2,kind=kind)
		print('{}\t-> {:.3f}'.format(kind,s))

def test4():
	X1 = [set(combinations(10000,50)) for i in range(10)]
	X2 = [set(combinations(10000,50)) for i in range(10)]
	Y1 = [1 for x in X1]
	Y2 = [0 for x in X2]
	# learning
	nn = rsm(10,5,c=5,boost=True)
	for i in range(10):
		nn.fit(X1+X2,Y1+Y2)
	# score
	for kind in ['f1','acc','prec','sens','spec']:
		s = nn.score(X1+X2,Y1+Y2,kind=kind)
		print('{}\t-> {:.3f}'.format(kind,s))
	print(nn.stats('win'))
	print(nn.stats('ctx'))
	print(nn.ctx)
if __name__=="__main__":
	test4()
