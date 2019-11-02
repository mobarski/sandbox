from pprint import pprint

import os
import pickle
import re
from collections import Counter
from random import shuffle,seed

# source: https://archive.ics.uci.edu/ml/machine-learning-databases/reuters_transcribed-mld/

ROOT = 'data/reuters_transcribed-mld'
ROOT = 'data/20_newsgroups'

LIMIT = 100

C1 = 'sci.space'
C2 = 'rec.motorcycles'

seed(44)

def text_by_cls():
	out = {}
	#for cls in os.listdir(ROOT):
	for cls in [C1,C2]:
		out[cls] = []
		path = os.path.join(ROOT,cls)
		filenames = os.listdir(path)
		shuffle(filenames)
		for fn in filenames[:LIMIT]:
			raw = open(os.path.join(path,fn)).read()
			out[cls] += [raw]
	return out
TEXT_BY_CLS = text_by_cls()

def doc_iter():
	for docs in TEXT_BY_CLS.values():
		for doc in docs:
			yield doc

digit_re = re.compile('[0-9]')
def token_iter(docs):
	for doc in docs:
		for t in re.findall('[\w.-]+',doc):
			if digit_re.findall(t): continue
			if '.' in t: continue
			t = t.lower()
			yield t

tf = Counter(token_iter(doc_iter()))
tokens = [t for t,_ in tf.most_common()]
t_by_i = {i+1:t for i,t in enumerate(tokens)}
i_by_t = {t:i+1 for i,t in enumerate(tokens)}

def vec_by_cls():
	out = {}
	for cls,docs in TEXT_BY_CLS.items():
		out[cls] = []
		for doc in docs:
			tokens = list(token_iter([doc]))
			vec = [i_by_t[t] for t in tokens if tf[t]>=2]
			out[cls] += [vec]
	return out

def learn_test_split(nl,nt=None):
	vbc = vec_by_cls()
	# X,Y
	X1 = [v for v in vbc[C1]]
	X2 = [v for v in vbc[C2]]
	Y1 = [1 for x in X1]
	Y2 = [0 for x in X2]
	# split
	X1L = X1[:nl]
	X1T = X1[nl:][:nt]
	X2L = X2[:nl]
	X2T = X2[nl:][:nt]
	Y1L = Y1[:nl]
	Y1T = Y1[nl:][:nt]
	Y2L = Y2[:nl]
	Y2T = Y2[nl:][:nt]
	return X1L,X2L,Y1L,Y2L,X1T,X2T,Y1T,Y2T

if __name__=="__main__":
	for k in vec_by_cls().keys():
		print(k)
