from __future__ import print_function
from v8 import *

def test5():
	from test_data import learn_test_split,t_by_i,tf
	X1L,X2L,Y1L,Y2L,X1T,X2T,Y1T,Y2T = learn_test_split(80)
	XL = X1L+X2L
	YL = Y1L+Y2L
	XT = X1T+X2T
	YT = Y1T+Y2T
	# learning
	nn = rsm(30,m=3,v=300,k=4,dropout=0.5)#,cutoff=0.1)
	for i in range(50):
		nn.fit2(X1L, X2L)
		# current score
		kind = 'f1'
		sl = nn.score(XL, YL, kind=kind)
		st = nn.score(XT, YT, kind=kind)
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
		tvec = [t_by_i.get(i,i) for i in vec]
		fvec = [tf.get(t,-1) for t in tvec]
		print(tvec,fvec) 
	# score
	print()
	nn.set_params(k=1)
	for kind in ['f1','acc','prec','sens','spec']:
		s = nn.score(XT, YT, kind=kind)
		print('{}\t-> {:.3f}'.format(kind,s))
	# win
	print()
	print(nn.win[1])
	print(nn.win[0])
	
if __name__=="__main__":
	test5()
