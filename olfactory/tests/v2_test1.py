from __future__ import print_function
import sys; sys.path.append('..')
from v2 import *

NI = 40
NN = 2000
NC = 6
NX = 10

nn = onn(NI,NN,NC)

X1 = [random_vector(0,255,NI) for _ in range(NX)]
X2 = [random_vector(0,255,NI) for _ in range(NX)]

def score_X1_X2():
	for X in [X1,X2]:
		print()
		for i,x in enumerate(X):
			s = nn.score(x)
			print(i,sum(top(10,s,values=True)))

print('\nBEFORE:')
score_X1_X2()

print('\nLEARNING:')
for _ in range(20):
	for x in X1:
		nn.learn(x,10)
		print('.',end='')
		sys.stdout.flush()
print()

print('\nAFTER:')
score_X1_X2()
