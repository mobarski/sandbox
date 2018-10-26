from multiprocessing import Pool
from collections import Counter
from itertools import groupby
from math import log
import re

def get_df_part(kwargs):
	X = kwargs['X']
	token_pattern = kwargs['token_pattern']
	stop_words = kwargs['stop_words']
	lowercase = kwargs['lowercase']
	encoding = kwargs['encoding']
	decode_error = kwargs['decode_error']
	p_min_df = kwargs['p_min_df']
	p_max_df = kwargs['p_max_df']
	d_min_tf = kwargs['d_min_tf']
	ngram_range = kwargs['ngram_range']
	analyzer = kwargs['analyzer']
	preprocessor = kwargs['preprocessor']
	tokenizer = kwargs['tokenizer']
	
	stop_words_set = set(stop_words or [])
	re_tok = re.compile(token_pattern,re.U)
	df = Counter()
	for text in X:
		# prepare tokens
		if encoding:
			text = text.decode(encoding,decode_error)
		if preprocessor:
			text = preprocessor(text)
		if lowercase:
			text = text.lower()
		if tokenizer:
			tokens = tokenizer(text)
		else:
			tokens = re_tok.findall(text)
		if stop_words:
			tokens = [t for t in tokens if t not in stop_words_set]
		
		# update df
		if ngram_range:
			lo,hi = ngram_range
			ngrams = []
			if analyzer=='word':
				for i in range(len(tokens)-lo): # TEST off-by-one
					for n in range(lo,hi+1):
						if i+n>len(tokens): break # TEST off-by-one
						ngrams.append(tuple(tokens[i:i+n])) # TODO tuple vs string
			elif analyzer=='char':
				for t in tokens:
					for n in range(lo,hi+1):
						if len(t)<n: pass
						elif len(t)==n:
							ngrams.append(t)
						else:
							for i in range(len(t)-n+1):
								ngrams.append(t[i:i+n])
			tokens = ngrams
		if d_min_tf:
			unique_tokens = [t for t,f in Counter(tokens).items() if f>=d_min_tf]
		else:
			unique_tokens = set(tokens)
		df.update(unique_tokens)
	
	# limit within partition
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

# TODO rename p_max_df->max_df_part d_min_tf->min_tf_doc
# TODO rename chi variables
# TODO option to include whole words shorter than char ngram_range 'lo' value
# TODO option to mark word begin/end in char ngrams
# TODO max_df float
# TODO max_df int
# TODO p_max_df float
# TODO min_df float
# TODO reorder ARGS
def get_df(X, workers=4, token_pattern='[\w][\w-]*', encoding='utf8', 
	   lowercase=True, min_df=0, p_min_df=0, max_df=1.0, p_max_df=1.0,
	   analyzer='word', tokenizer=None, preprocessor=None,
	   decode_error='strict', stop_words=None, mp_pool=None,
	   d_min_tf=0, ngram_range=None):
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
				,analyzer = analyzer
				,ngram_range = ngram_range
				,tokenizer = tokenizer
				,preprocessor = preprocessor
				,decode_error = decode_error
				,stop_words = stop_words
				,d_min_tf = d_min_tf
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

### 24s get_dfy vs 11s get_df vs 25s get_dfy2(specialized)
def get_dfy(X,Y,workers=4,mp_pool=None,**kwargs):
	dfy = {}
	data = sorted(zip(Y,X))
	pool = mp_pool or Pool(workers)
	for y,g in groupby(data,lambda x:x[0]):
		x = [v[1] for v in g]
		dfy[y] = get_df(x,mp_pool=pool,**kwargs)
	return dfy

def get_df_from_dfy(dfy):
	df = Counter()
	for y in dfy:
		df.update(dfy[y])
	return df

# ---[ feature selection ]------------------------------------------------------

def get_idf(df, n, a1=1, a2=1, a3=1, min_df=0):
	idf = Counter()
	for t in df:
		if min_df and df[t]<min_df: continue
		idf[t] = log( (a1+n) / (a2+df[t]) ) + a3
	return idf

def get_chi(df,n,dfy,ny,alpha=0):
	chi = Counter()
	all = df
	topic = dfy
	for t in df:
		# observed
		o_c1_t1 = topic[t]
		o_c1_t0 = ny - topic[t]
		o_c0_t1 = all[t] - topic[t]
		o_c0_t0 = n - o_c1_t1 - o_c1_t0 - o_c0_t1
		# expected
		e_c1_t1 = 1.0 * ny * all[t]/n
		e_c1_t0 = 1.0 * ny * (n-all[t])/n
		e_c0_t1 = 1.0 * (n-ny)/n * all[t]
		e_c0_t0 = 1.0 * (n-ny)/n * (n-all[t])
		# chi components
		c1_t1 = (o_c1_t1 - e_c1_t1)**2 / (e_c1_t1 + alpha)
		c1_t0 = (o_c1_t0 - e_c1_t0)**2 / (e_c1_t0 + alpha)
		c0_t1 = (o_c0_t1 - e_c0_t1)**2 / (e_c0_t1 + alpha)
		c0_t0 = (o_c0_t0 - e_c0_t0)**2 / (e_c0_t0 + alpha)
		# chi
		chi[t] = c0_t0 + c1_t0 + c0_t1 + c1_t1
	return chi

def get_chi_explain(df,n,dfy,ny,alpha=0):
	chi_explain = dict()
	all = df
	topic = dfy
	for t in df:
		# observed
		o_c1_t1 = topic[t]
		o_c1_t0 = ny - topic[t]
		o_c0_t1 = all[t] - topic[t]
		o_c0_t0 = n - o_c1_t1 - o_c1_t0 - o_c0_t1
		# expected
		e_c1_t1 = 1.0 * ny * all[t]/n
		e_c1_t0 = 1.0 * ny * (n-all[t])/n
		e_c0_t1 = 1.0 * (n-ny)/n * all[t]
		e_c0_t0 = 1.0 * (n-ny)/n * (n-all[t])
		# chi components
		c1_t1 = (o_c1_t1 - e_c1_t1)**2 / (e_c1_t1 + alpha)
		c1_t0 = (o_c1_t0 - e_c1_t0)**2 / (e_c1_t0 + alpha)
		c0_t1 = (o_c0_t1 - e_c0_t1)**2 / (e_c0_t1 + alpha)
		c0_t0 = (o_c0_t0 - e_c0_t0)**2 / (e_c0_t0 + alpha)
		# chi
		chi = c0_t0 + c1_t0 + c0_t1 + c1_t1
		# explain
		ex = dict()
		ex['o_c1_t1'] = o_c1_t1
		ex['o_c1_t0'] = o_c1_t0
		ex['o_c0_t1'] = o_c0_t1
		ex['o_c0_t0'] = o_c0_t0
		ex['e_c1_t1'] = e_c1_t1
		ex['e_c1_t0'] = e_c1_t0
		ex['e_c0_t1'] = e_c0_t1
		ex['e_c0_t0'] = e_c0_t0
		ex['c1_t1']   = c1_t1
		ex['c1_t0']   = c1_t0
		ex['c0_t1']   = c0_t1
		ex['c0_t0']   = c0_t0
		ex['chi']     = chi
		ex = {k:int(v) for k,v in ex.items()}
		chi_explain[t] = ex
	return chi_explain
	
# ------------------------------------------------------------------------------

if __name__ == "__main__":
	import pandas as pd
	from time import time
	import pickle

	def my_preproc(text):
		return text.lower()
	
	test_re = re.compile(r'\ba\w{4,6}\b',re.U)
	def my_tokenizer(text):
		return test_re.findall(text)
	
	if 1:
		frame = pd.read_csv('flat/__all__.txt',sep='\t',header=None,names=['col','id','text'])
		t0=time()
		#df = get_df(frame.text,12,min_df=10,max_df=0.5)
		dfy = get_dfy(frame.text,frame.col,workers=12,min_df=10,analyzer='char',ngram_range=(3,4))
		for y in dfy:
			print(y,len(dfy[y]))
		print(time()-t0)
		
		t0=time()
		df = get_df_from_dfy(dfy)
		topic = 'ogrod'
		chi = get_chi(df,len(frame.text),dfy[topic],Counter(frame.col)[topic])
		chi_ex = get_chi_explain(df,len(frame.text),dfy[topic],Counter(frame.col)[topic])
		for t,v in chi.most_common(100):
			print(t,v,df[t],chi_ex[t])
		print(len(df))
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
