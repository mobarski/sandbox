from multiprocessing import Pool
from collections import Counter
from itertools import groupby
from math import log
import re

def get_df_part(kwargs):
	X = kwargs['X']
	token_pattern = kwargs['token_pattern']
	lowercase = kwargs['lowercase']
	encoding = kwargs['encoding']
	p_min_df = kwargs['p_min_df']
	p_max_df = kwargs['p_max_df']
	char_ngram_range = kwargs['char_ngram_range']
	tokenizer = kwargs['tokenizer']
	
	re_tok = re.compile(token_pattern,re.U)
	df = Counter()
	for text in X:
		text = text.decode(encoding)
		if lowercase:
			text = text.lower()
		tokens = re_tok.findall(text)
		if char_ngram_range:
			lo,hi = char_ngram_range
			ngrams = []
			for t in tokens:
				for n in range(lo,hi+1):
					if len(t)<n: pass
					elif len(t)==n:
						ngrams.append(t)
					else:
						for i in range(len(t)-n+1):
							ngrams.append(t[i:i+n])
			df.update(set(ngrams))
		else:
			df.update(set(tokens))
	if p_min_df:
		below = [t for t in df if df[t]<p_min_df]
		for t in below:
			del df[t]
	if p_max_df < 1.0:
		x = p_max_df * len(X)
		above = [t for t in df if df[t]>x]
		for t in above:
			del df[t]
	return df

def get_dfy_part(kwargs):
	X = kwargs['X']
	Y = kwargs['Y']
	token_pattern = kwargs['token_pattern']
	lowercase = kwargs['lowercase']
	encoding = kwargs['encoding']
	char_ngram_range = kwargs['char_ngram_range']
	tokenizer = kwargs['tokenizer']
	
	re_tok = re.compile(token_pattern,re.U)
	dfy = {y:Counter() for y in set(Y)}
	for text,y in X,Y:
		text = text.decode(encoding)
		if lowercase:
			text = text.lower()
		tokens = re_tok.findall(text)
		if char_ngram_range:
			lo,hi = char_ngram_range
			ngrams = []
			for t in tokens:
				for n in range(lo,hi+1):
					if len(t)<n: pass
					elif len(t)==n:
						ngrams.append(t)
					else:
						for i in range(len(t)-n+1):
							ngrams.append(t[i:i+n])
			dfy[y].update(set(ngrams))
		else:
			dfy[y].update(set(tokens))

	return dfy

# TODO min_df float
# TODO max_df float
# TODO p_max_df float
# TODO max_df int
# TODO stop_words
# TODO decode_error
# TODO tokenizer <- lematize
# TODO strip_accents
# TODO preprocessor <- strip_accents
# TODO word_ngram_range
def get_df(X, workers=4, token_pattern='[\w][\w-]*', encoding='utf8', lowercase=True, min_df=0, p_min_df=0, max_df=1.0, p_max_df=1.0, char_ngram_range=None, tokenizer=None, mp_pool=None):
	cnt = len(X)
	
	data = []
	n = cnt/workers # TEST off-by-one
	pos = 0
	for i in range(workers):
		lo = pos
		hi = min(cnt-1,lo+n)
		kwargs = dict(
				X = X[lo:hi]
				,token_pattern = token_pattern
				,encoding = encoding
				,lowercase = lowercase
				,p_min_df = p_min_df
				,p_max_df = p_max_df
				,char_ngram_range = char_ngram_range
				,tokenizer = tokenizer
			)
		data.append(kwargs)
		pos += n
	
	pool = mp_pool or Pool(workers)
	df_partitions = pool.map(get_df_part, data)
	df=df_partitions[0]
	for df_ in df_partitions[1:]:
		df.update(df_)
	
	if min_df:
		below = [t for t in df if df[t]<min_df]
		for t in below:
			del df[t]
	if max_df < 1.0:
		max_df_cnt = max_df * len(X)
		above = [t for t in df if df[t]>max_df_cnt]
		for t in above:
			del df[t]
	return df

def get_dfy2(X, Y, workers=4, token_pattern='[\w][\w-]*', encoding='utf8', lowercase=True, min_df=0, p_min_df=0, max_df=1.0, p_max_df=1.0, char_ngram_range=None, tokenizer=None, mp_pool=None):
	cnt = len(X)
	
	data = []
	n = cnt/workers # TEST off-by-one
	pos = 0
	for i in range(workers):
		lo = pos
		hi = min(cnt-1,lo+n)
		kwargs = dict(
				X = X[lo:hi]
				,Y = Y[lo:hi]
				,token_pattern = token_pattern
				,encoding = encoding
				,lowercase = lowercase
				,p_min_df = p_min_df
				,p_max_df = p_max_df
				,char_ngram_range = char_ngram_range
				,tokenizer = tokenizer
			)
		data.append(kwargs)
		pos += n
	
	pool = mp_pool or Pool(workers)
	dfy_partitions = pool.map(get_dfy_part, data)
	
	dfy = {y:Counter() for y in set(Y)}
	for y in dfy_partitions[0]:
		dfy[y] = dfy_partitions[0][y]
	
	for dfy_ in dfy_partitions[1:]:
		for y in dfy_:
			dfy[y].update(dfy_[y])

	for y in dfy:
		df = dfy[y]
		if min_df:
			below = [t for t in df if df[t]<min_df]
			for t in below:
				del df[t]
		if max_df < 1.0:
			max_df_cnt = max_df * len(X)
			above = [t for t in df if df[t]>max_df_cnt]
			for t in above:
				del df[t]
	return dfy

def get_idf(df, n, s1=1, s2=1, s3=1, min_df=0):
	idf = Counter()
	for t in df:
		if min_df and df[t]<min_df: continue
		idf[t] = log( (s1+n) / (s2+df[t]) ) + s3
	return idf

### 24s get_dfy vs 11s get_df vs 25s get_dfy2(specialized)
def get_dfy(X,Y,workers=4,**kwargs):
	dfy = {}
	data = sorted(zip(Y,X))
	pool = Pool(workers)
	for y,g in groupby(data,lambda x:x[0]):
		x = [v[1] for v in g]
		dfy[y] = get_df(x,mp_pool=pool,**kwargs)
	return dfy
	
# TODO get_chi(df,dfy) lub (dfy)
	
# ------------------------------------------------------------------------------

if __name__ == "__main__":
	import pandas as pd
	from time import time
	import pickle

	if 1:
		frame = pd.read_csv('flat/__all__.txt',sep='\t',header=None,names=['col','id','text'])
		t0=time()
		#df = get_df(frame.text,12,min_df=10,max_df=0.5)
		dfy = get_dfy(frame.text,frame.col,workers=12,min_df=10)
		for y in dfy:
			print(y,len(dfy[y]))
		print(time()-t0)
		# n = len(frame.text)
		# print(len(df))
		# pickle.dump([df,n],open('df_n.pickle','wb'))
	else:
		df,n = pickle.load(open('df_n.pickle','rb'))
	
	# print(min(df.values()))
	# for t,v in df.most_common(10):
		# print(t,v)
	
	# t0=time()
	# idf = get_idf(df,n,min_df=10)
	# for t,v in idf.most_common(10):
		# print(t,v,df[t])
	# print(time()-t0)
