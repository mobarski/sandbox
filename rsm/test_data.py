from pprint import pprint

import os
import pickle
import re
from collections import Counter

# source: https://archive.ics.uci.edu/ml/machine-learning-databases/reuters_transcribed-mld/

ROOT = 'data/reuters_transcribed-mld'
ROOT = 'data/20_newsgroups'

LIMIT = 100

def text_by_cls():
	out = {}
	#for cls in os.listdir(ROOT):
	for cls in ['sci.space','rec.motorcycles']:
		out[cls] = []
		path = os.path.join(ROOT,cls)
		for fn in os.listdir(path)[:LIMIT]:
			raw = open(os.path.join(path,fn)).read()
			out[cls] += [raw]
	return out

def doc_iter():
	for docs in text_by_cls().values():
		for doc in docs:
			yield doc

def token_iter(docs):
	for doc in docs:
		for t in re.findall('[\w.-]+',doc):
			if t[-1]=='.':
				t=t[:-1]
			t = t.lower()
			yield t

tf = Counter(token_iter(doc_iter()))
tokens = [t for t,_ in tf.most_common()]
t_by_i = {i+1:t for i,t in enumerate(tokens)}
i_by_t = {t:i+1 for i,t in enumerate(tokens)}

def vec_by_cls():
	out = {}
	for cls,docs in text_by_cls().items():
		out[cls] = []
		for doc in docs:
			tokens = list(token_iter([doc]))
			vec = [i_by_t[t] for t in tokens]
			out[cls] += [vec]
	return out


if __name__=="__main__":
	for k in vec_by_cls().keys():
		print(k)
