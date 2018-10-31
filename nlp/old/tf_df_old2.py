import pandas as pd
from collections import Counter
import re
from multiprocessing import Pool
from math import log

from time import time
import pickle

frame = pd.read_csv('flat/__all__.txt',sep='\t',header=None,names=['col','id','text'])

def tf_df_part(kwargs):
	iterable = kwargs['iterable']
	token_pattern = kwargs['token_pattern']
	lowercase = kwargs['lowercase']
	encoding = kwargs['encoding']
	p_min_df = kwargs['p_min_df']
	p_max_df = kwargs['p_max_df']
	char_ngram_range = kwargs['char_ngram_range']
	tokenizer = kwargs['tokenizer']
	
	re_tok = re.compile(token_pattern,re.U)
	tf = Counter()
	df = Counter()
	for text in iterable:
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
			tf.update(ngrams)
			df.update(set(ngrams))
		else:
			tf.update(tokens)
			df.update(set(tokens))
	if p_min_df:
		below = [t for t in df if df[t]<p_min_df]
		for t in below:
			del tf[t]
			del df[t]
	if p_max_df < 1.0:
		x = p_max_df * len(iterable)
		above = [t for t in df if df[t]>x]
		for t in above:
			del tf[t]
			del df[t]
	return tf,df

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
def get_tf_df(iterable, workers=4, token_pattern='[\w][\w-]*', encoding='utf8', lowercase=True, min_df=0, p_min_df=0, max_df=1.0, p_max_df=1.0, char_ngram_range=None, tokenizer=None):
	cnt = len(iterable)
	
	data = []
	n = cnt/workers # TEST off-by-one
	x = 0
	for i in range(workers):
		lo = x
		hi = min(cnt-1,lo+n)
		kwargs = dict(
				iterable = iterable[lo:hi]
				,token_pattern = token_pattern
				,encoding = encoding
				,lowercase = lowercase
				,p_min_df = p_min_df
				,p_max_df = p_max_df
				,char_ngram_range = char_ngram_range
				,tokenizer = tokenizer
			)
		data.append(kwargs)
		x += n
	
	pool = Pool(workers)
	tf_df = pool.map(tf_df_part, data)
	tf,df=tf_df[0]
	for tf_,df_ in tf_df[1:]:
		tf.update(tf_)
		df.update(df_)
	
	if min_df:
		below = [t for t in df if df[t]<min_df]
		for t in below:
			del tf[t]
			del df[t]
	if max_df < 1.0:
		x = max_df * len(iterable)
		above = [t for t in df if df[t]>x]
		for t in above:
			del tf[t]
			del df[t]
	return tf,df

def get_idf(df, n, s1=1, s2=1, s3=1, min_df=0):
	idf = Counter()
	for t in df:
		if min_df and df[t]<min_df: continue
		idf[t] = log( (s1+n) / (s2+df[t]) ) + s3
	return idf

# TODO get_chi
	
# ------------------------------------------------------------------------------

if __name__ == "__main__":
	t0=time()
	tf,df = get_tf_df(frame.text,12,min_df=10,max_df=0.5)
	n = len(frame.text)
	print(len(df),len(tf))
	print(time()-t0)
	pickle.dump([tf,df,n],open('tf_df_n.pickle','wb'))
	#tf,df,n = pickle.load(open('tf_df_n.pickle','rb'))
	print(min(df.values()))
	for t,x in df.most_common(10):
		print(t,x)
	
	t0=time()
	idf = get_idf(df,n,min_df=10)
	for t,x in idf.most_common(10):
		print(t,x,tf[t],df[t])
	print(time()-t0)
