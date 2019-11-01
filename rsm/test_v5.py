from v5 import *

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
	print(list(nn.ctx))

def test5():
	from test_data import vec_by_cls,t_by_i
	vbc = vec_by_cls()
	# X,Y
	X1 = [set(v) for v in vbc['sci.space']]
	X2 = [set(v) for v in vbc['rec.motorcycles']]
	Y1 = [1 for x in X1]
	Y2 = [0 for x in X2]
	# split
	p = 50
	X1L = X1[:p]
	X1T = X1[p:]
	X2L = X2[:p]
	X2T = X2[p:]
	Y1L = Y1[:p]
	Y1T = Y1[p:]
	Y2L = Y2[:p]
	Y2T = Y2[p:]
	# learning
	nn = rsm(200,3,c=0,k=20,cutoff=0.1,method=1)
	for i in range(100):
		#nn.fit(X1L+X2L, Y1L+Y2L)
		nn.fit2(X1L, X2L)
	#
	for j in range(1,20):
		vec = nn.mem[j]
		print [t_by_i[i] for i in vec]
	# score
	nn.set_params(k=1)
	for kind in ['f1','acc','prec','sens','spec']:
		s = nn.score(X1T+X2T, Y1T+Y2T, kind=kind)
		print('{}\t-> {:.3f}'.format(kind,s))
	print(nn.stats('win'))
	print(nn.stats('mem'))
	print(list(nn.ctx))
	nn.calibrate(X1+X2, Y1+Y2,'f1')



if __name__=="__main__":
	test5()
