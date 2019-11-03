from __future__ import print_function
from v8 import *

seed(44)

def test5():
	from test_data import learn_test_split,t_by_i,tf
	X1L,X2L,Y1L,Y2L,X1T,X2T,Y1T,Y2T = learn_test_split(160)
	XL = X1L+X2L
	YL = Y1L+Y2L
	XT = X1T+X2T
	YT = Y1T+Y2T
	print(sum([len(x) for x in XL]))
	t0 = time()
	# learning

	nn = rsm(80, m=40, v=20, k=2, boost=2,
			dropout=0.5, decay=0.005,
			c=20, sequence=1,
			awidth=10, astep=10,
			cutoff=0.01)
			
	for i in range(13):
		nn.fit2(X1L, X2L)
		# current score
		kind = 'f1'
		sl = nn.score(XL, YL, kind=kind)
		st = nn.score(XT, YT, kind=kind)
		print('{}\t{}  ->  {:.3f}   {:.3f}'.format(i+1,kind,sl,st)); sys.stdout.flush()
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
	print('\nCNT:')
	for j in range(1,20):
		vec = nn.cnt[j].most_common()
		tvec = [(t_by_i.get(i,i),c) for i,c in vec]
		fvec = [tf.get(t,-1) for t,c in tvec]
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
	#
	print()
	print(time()-t0)
	#
	print()
	nn.calibrate(XT,YT)
	#
	from test_data import biker_vec
	print('biker mice from mars score:')
	print(nn.transform_one_v3(biker_vec))
	
if __name__=="__main__":
	test5()
