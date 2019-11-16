from v5 import *

def test5():
	from test_data import learn_test_split,t_by_i
	X1L,X2L,Y1L,Y2L,X1T,X2T,Y1T,Y2T = learn_test_split(10)
	# learning
	nn = rsm(20,5,c=5,k=2,cutoff=0.1,method=1)
	for i in range(20):
		#nn.fit(X1L+X2L, Y1L+Y2L)
		nn.fit2(X1L, X2L)
	#
	for j in range(1,20):
		vec = nn.mem[j]
		print [t_by_i.get(i,i) for i in vec]
	# score
	nn.set_params(k=1)
	for kind in ['f1','acc','prec','sens','spec']:
		s = nn.score(X1T+X2T, Y1T+Y2T, kind=kind)
		print('{}\t-> {:.3f}'.format(kind,s))
	print(nn.stats('win'))
	print(nn.stats('ctx'))
	print(list(nn.ctx))
	nn.calibrate(X1T+X2T, Y1T+Y2T,'f1')



if __name__=="__main__":
	test5()
