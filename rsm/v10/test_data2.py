from pprint import pprint

import os
import pickle
import re
from collections import Counter
from random import shuffle,seed


# ---[ HIGH LEVEL ]-------------------------------------------------------------



# ---[ LOW LEVEL ]--------------------------------------------------------------

ROOT = '../data/20_newsgroups'
def get_docs(cls,*n_list):
	"return n documents from selected class"
	all = []
	path = os.path.join(ROOT,cls)
	filenames = os.listdir(path)
	shuffle(filenames)
	for fn in filenames[:sum(n_list)]:
		raw = open(os.path.join(path,fn)).read()
		all += [raw]
	out = []
	rest = all
	for n in n_list:
		head,rest = rest[:n],rest[n:]
		out += [head]
	print('DOCS: {} -> {}'.format(cls,[len(x) for x in out]))
	return out

# ---[ UTIL ]-------------------------------------------------------------------

digit_re = re.compile('[0-9]')
token_re = re.compile('[\w.-]+')
def token_iter(docs):
	"iterate over all tokens from docs"
	for doc in docs:
		for t in re.findall(token_re,doc):
			if digit_re.findall(t): continue
			if '.' in t: continue
			t = t.lower()
			yield t

def get_tf(min_tf,*corpora):
	tf = Counter()
	for corpus in corpora:
		for doc in corpus:
			_tf = Counter(token_iter([doc]))
			tf.update(**{t:f for t,f in _tf.items() if f>=min_tf})
	return tf

def get_df(min_tf,*corpora):
	df = Counter()
	for corpus in corpora:
		for doc in corpus:
			tf = Counter(token_iter([doc]))
			df.update(set([t for t,f in tf.items() if f>=min_tf]))
	return df

def get_dictionary(tokens):
	return {t:i+1 for i,t in enumerate(tokens)}

def reverse_dict(d):
	out = {}
	for k,v in d.items():
		out[v] = k
	return out

def get_encoded(d,*corpora):
	out = []
	for docs in corpora:
		corpus = []
		for doc in docs:
			encoded = []
			for token in token_iter([doc]):
				if token in d:
					encoded += [d[token]]
			corpus += [encoded]
		out += [corpus]
	return out

# ---[ MAIN ]-------------------------------------------------------------------

if __name__=="__main__":
	seed(1)
	X = get_docs('comp.windows.x',2)[0]
	for x in X:
		print(x)
	tf = get_tf(2,X)
	df = get_df(2,X)
	pprint(tf)
	pprint(df)
	tokens = [t for t,f in tf.items() if f>1]
	d = get_dictionary(tokens)
	di = reverse_dict(d)
	pprint(d)
	pprint(di)
	X = get_encoded(d,X)[0]
	pprint(X)
	