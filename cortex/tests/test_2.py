from __future__ import print_function
import sys; sys.path.append('..')
from core import *

if __name__=="__main__":
	if 1:
		from pprint import pprint
		print("TEST agg_score\n")
		N = 64
		K = 6
		sp = spatial_pooler(N,K,u=0.5,p_inc=21,boost=True)
		X1 = [random_sdr(N,K) for _ in range(10)]
		X2 = [random_sdr(N,K) for _ in range(10)]
		
		for _ in range(1000):
			for x in X1:
				sp.learn(x,dynamic=False)
		print(sp.activity)
		print()

		for limit in [None,K//2]:
			print("LIMIT: {}".format(limit))
			for X in [X1,X2]:
				print()
				for i,x in enumerate(X):
					s = sp.agg_score(set(list(x)[:limit]))
					print("{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}".format(i,s['pct_max'],s['pct_q1'],s['pct_q2'],s['pct_q3'],s['pct_min']))
				print()
			
		print('\nACTIVITY:\n')
		pprint(sp.agg_activity())
		print('\nPERMANENCE:\n')
		pprint(sp.agg_perm())
		
	