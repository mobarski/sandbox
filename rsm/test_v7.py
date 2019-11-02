from __future__ import print_function
from v7 import *

def test5():
	from test_data import learn_test_split,t_by_i,tf
	X1L,X2L,Y1L,Y2L,X1T,X2T,Y1T,Y2T = learn_test_split(30)
	# learning
	nn = rsm(100,5,c=0,v=5,k=6,dropout=0.5,cutoff=0.1,method=1)
	for i in range(40):
		#nn.fit(X1L+X2L, Y1L+Y2L)
		nn.fit2(X1L, X2L)
		#
		kind = 'f1'
		sl = nn.score(X1L+X2L, Y1L+Y2L, kind=kind)
		st = nn.score(X1T+X2T, Y1T+Y2T, kind=kind)
		print('{}  ->  {:.3f}   {:.3f}'.format(kind,sl,st)); sys.stdout.flush()
	#
	print('\nMEM:')
	for j in range(1,20):
		vec = nn.mem[j]
		tvec = [t_by_i.get(i,i) for i in vec]
		fvec = [tf.get(t,-1) for t in tvec]
		print(tvec,fvec) 
	print('\nNEG:')
	for j in range(1,20):
		vec = nn.neg[j]
		print([t_by_i.get(i,i) for i in vec])
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
