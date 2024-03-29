from __future__ import print_function
from v10 import *

seed(44)
ITERS = 11
	
def test5():
	N1L = 380; N1T=20; C1 = 'comp.sys.mac.hardware'
	N2L = 380; N2T=20; C2 = 'comp.windows.x'

	# INIT
	
	t0 = time()
	from test_data2 import get_docs, get_df, get_tf, get_dictionary, reverse_dict, get_encoded
	
	X1L,X1T = get_docs(C1, N1L, N1T)
	X2L,X2T = get_docs(C2, N2L, N2T)
	
	df = get_df(2,X1L,X2L)
	selected = [t for t,f in df.items() if f>=2] # TODO remove upper extremum
	dictionary = get_dictionary(selected)
	
	t_by_i = reverse_dict(dictionary)	
	tf = get_tf(X1L,X2L)
	
	X1L,X1T,X2L,X2T = get_encoded(dictionary, X1L, X1T, X2L, X2T)
	Y1L = [1]*N1L
	Y2L = [0]*N2L
	Y1T = [1]*N1T
	Y2T = [0]*N2T

	# # #
	
	XL = X1L+X2L
	YL = Y1L+Y2L
	XT = X1T+X2T
	YT = Y1T+Y2T
	
	print('\nLEARN tokens: {}'.format(sum([len(x) for x in XL])))
	print('\nINIT done in {:.2f}s\n'.format(time()-t0))

	# MODEL

	nn = rsm(n=80, m=80, v=80, k=2,
			boost_free=0.0, boost_rare=0.9, noise=0.0,
			dropout=0.5, penalty=3,
			c=0, sequence=0,
			awidth=10, astep=10,
			cutoff=0.01,
			activation=2)

	# LEARNING
	t0 = time()
	for i in range(ITERS):
		nn.fit2(X1L, X2L)
		# current score
		kind = 'f1'
		sl = nn.score(XL, YL, kind=kind)
		st = nn.score(XT, YT, kind=kind)
		# current stats
		g1 = gini(nn.win[1].values())
		used = sum([len(m)>0 for m in nn.mem.values()])
		free = sum([len(m)==0 for m in nn.mem.values()])
		full = sum([len(m)==80 for m in nn.mem.values()])
		print('{}\t{}  ->  {:.3f}   {:.3f}  \t  gini -> {:.3f}  \t  used -> {}  \t  free -> {}  \t  full -> {}'.format(i+1,kind,sl,st,g1,used,free,full)); sys.stdout.flush()
	print('\nLEARNING done in {:.2f}s'.format(time()-t0))
	
	# INFO
	if 0:
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
	
	# SCORE
	print()
	nn.set_params(k=1)
	for kind in ['f1','acc','prec','sens','spec']:
		s = nn.score(XT, YT, kind=kind)
		print('{}\t-> {:.3f}'.format(kind,s))
	
	# WIN
	print('\nWIN:')
	w1 = nn.win[1].values()
	w0 = nn.win[0].values()
	print('[1] -> gini:{:.3f}  min:{}  max:{}'.format(gini(w1), min(w1), max(w1)))
	print('[0] -> gini:{:.3f}  min:{}  max:{}'.format(gini(w0), min(w0), max(w0)))
	
	# CALIBRATION
	print()
	t0=time()
	nn.calibrate2(XL,YL,XT,YT)
	print('\nCALIBRATION done in {:.2f}s\n'.format(time()-t0))

if __name__=="__main__":
	test5()
