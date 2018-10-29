from multiprocessing import Pool
from collections import Counter
from itertools import groupby
from math import log,ceil
import re

# TODO vectorize
# TODO wybieranie ngramow na podstawie liftu

# ---[ document frequency ]-----------------------------------------------------

# TODO test replacing Coutner with dict (marshaling + performance?)
def get_df_part(kwargs):
	X = kwargs['X']
	token_pattern = kwargs['token_pattern']
	stop_words = kwargs['stop_words']
	lowercase = kwargs['lowercase']
	encoding = kwargs['encoding']
	decode_error = kwargs['decode_error']
	min_df_part = kwargs['min_df_part']
	max_df_part = kwargs['max_df_part']
	min_tf_doc = kwargs['min_tf_doc']
	ngram_range = kwargs['ngram_range']
	ngram_words = kwargs['ngram_words']
	analyzer = kwargs['analyzer']
	preprocessor = kwargs['preprocessor']
	tokenizer = kwargs['tokenizer']
	postprocessor = kwargs['postprocessor']
	
	stop_words_set = set(stop_words or [])
	ngram_words_set = set(ngram_words or [])
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
		if postprocessor:
			tokens = postprocessor(tokens)
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
						ngram = tuple(tokens[i:i+n])
						if not ngram_words_set&set(ngram): continue
						ngrams.append(ngram) # TODO tuple vs string
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
		if min_tf_doc:
			unique_tokens = [t for t,f in Counter(tokens).items() if f>=min_tf_doc]
		else:
			unique_tokens = set(tokens)
		df.update(unique_tokens)
	
	# limit within partition
	if min_df_part:
		below = [t for t in df if df[t]<min_df_part]
		for t in below:
			del df[t]
	if max_df_part < 1.0:
		x = max_df_part * len(X)
		above = [t for t in df if df[t]>x]
		for t in above:
			del df[t]
	return df

# TODO rename max_df_part->max_df_part min_tf_doc->min_tf_doc
# TODO rename chi variables
# TODO option to include whole words shorter than char ngram_range 'lo' value
# TODO option to mark word begin/end in char ngrams
# TODO max_df float
# TODO max_df int
# TODO max_df_part float
# TODO min_df float
# TODO reorder ARGS
def get_df(X, workers=4, token_pattern='[\w][\w-]*', encoding='utf8', 
	   lowercase=True, min_df=0, min_df_part=0, max_df=1.0, max_df_part=1.0,
	   analyzer='word', tokenizer=None, preprocessor=None,
	   decode_error='strict', stop_words=None, mp_pool=None,
	   min_tf_doc=0, ngram_range=None, postprocessor=None, ngram_words=None):
	cnt = len(X)
	
	data = []
	n = int(ceil(1.0*cnt/workers))
	pos = 0
	for i in range(workers):
		lo = pos
		hi = min(cnt,lo+n)
		kwargs = dict(
				X = X[lo:hi]
				,token_pattern = token_pattern
				,encoding = encoding
				,lowercase = lowercase
				,min_df_part = min_df_part
				,max_df_part = max_df_part
				,analyzer = analyzer
				,ngram_range = ngram_range
				,tokenizer = tokenizer
				,preprocessor = preprocessor
				,decode_error = decode_error
				,stop_words = stop_words
				,min_tf_doc = min_tf_doc
				,postprocessor = postprocessor
				,ngram_words = ngram_words
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
def get_dfy(X,Y,workers=4,sort=True,mp_pool=None,**kwargs):
	dfy = {}
	if sort:
		data = sorted(zip(Y,X))
	else:
		data = zip(Y,X)
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

# ---[ vectorization ]----------------------------------------------------------

def vectorize_part(kwargs):
	
	vocabulary = kwargs['vocabulary']
	binary = kwargs['binary']
	sparse = kwargs['sparse']
	upper_limit = kwargs['upper_limit']
	
	dtype = kwargs['dtype']
	typecode = kwargs['typecode']
	if dtype:
		import numpy as np
	if typecode:
		from array import array
		from itertools import chain
	
	X = kwargs['X']
	token_pattern = kwargs['token_pattern']
	stop_words = kwargs['stop_words']
	lowercase = kwargs['lowercase']
	encoding = kwargs['encoding']
	decode_error = kwargs['decode_error']
	ngram_range = kwargs['ngram_range']
	ngram_words = kwargs['ngram_words']
	analyzer = kwargs['analyzer']
	preprocessor = kwargs['preprocessor']
	tokenizer = kwargs['tokenizer']
	postprocessor = kwargs['postprocessor']
	
	if hasattr(vocabulary,'items'):
		vocab_dict = vocabulary
		vocab_len = max(vocab_dict.values()) + 1
	else:
		vocab_dict = {t:t_id for t_id,t in enumerate(vocabulary)}
		vocab_len = len(vocabulary)
	out = []
	
	stop_words_set = set(stop_words or [])
	ngram_words_set = set(ngram_words or [])
	re_tok = re.compile(token_pattern,re.U)
	for ix,text in enumerate(X):
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
		if postprocessor:
			tokens = postprocessor(tokens)
		if stop_words:
			tokens = [t for t in tokens if t not in stop_words_set]
		
		# TODO filter tokens - keep only vocabulary -> here or after ngrams ???
		
		# ngrams
		if ngram_range:
			lo,hi = ngram_range
			ngrams = []
			if analyzer=='word':
				for i in range(len(tokens)-lo): # TEST off-by-one
					for n in range(lo,hi+1):
						if i+n>len(tokens): break # TEST off-by-one
						ngram = tuple(tokens[i:i+n])
						if not ngram_words_set&set(ngram): continue
						ngrams.append(ngram) # TODO tuple vs string
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
		
		# output
		if sparse:
			if binary:
				v = [vocab_dict[t] for t in set(tokens) if t in vocab_dict]
				if typecode:
					v = array(typecode,v)
				elif dtype:
					v = np.array(v,dtype=dtype)
			else:
				tf = {}
				for t in tokens:
					if t not in vocab_dict: continue
					t_id = vocab_dict[t]
					if t_id not in tf: tf[t_id]=1
					else:
						tf[t_id]+=1
				if upper_limit:
					for t in tf:
						tf[t] = min(upper_limit,tf[t])
				v = tf
				if typecode:
					v = array(typecode,chain.from_iterable(tf.items()))
				elif dtype:
					v = np.array(tf.items(),dtype=dtype)
		else:
			v = [0]*vocab_len
			if binary:
				for t in tokens:
					if t not in vocab_dict: continue
					t_id = vocab_dict[t]
					v[t_id] = 1
			else:
				for t in tokens:
					if t not in vocab_dict: continue
					t_id = vocab_dict[t]
					v[t_id] += 1
			if typecode:
				v = array(typecode, v)
			elif dtype:
				v = np.array(v, dtype=dtype)
			if upper_limit:
				if dtype:
					v.clip(1,upper_limit)
				elif dtype:
					for t_id in range(vocab_len):
						v[t_id] = min(upper_limit,v[t_id])
				else:
					v = [min(upper_limit,f) for f in v]
		out.append(v)
	return out

# TODO remove dead options
def vectorize(X, vocabulary, workers=4,
	   token_pattern='[\w][\w-]*', encoding='utf8', lowercase=True,
	   analyzer='word', tokenizer=None, preprocessor=None,
	   decode_error='strict', stop_words=None, mp_pool=None,
	   ngram_range=None, postprocessor=None, ngram_words=None,
	   binary=False, sparse=True, upper_limit=0,
	   typecode=None, dtype=None):
	cnt = len(X)
	
	data = []
	n = cnt/workers # TEST off-by-one
	pos = 0
	for i in range(workers):
		lo = pos
		hi = min(cnt,lo+n)
		kwargs = dict(
				X = X[lo:hi]
				,token_pattern = token_pattern
				,encoding = encoding
				,lowercase = lowercase
				,analyzer = analyzer
				,ngram_range = ngram_range
				,tokenizer = tokenizer
				,preprocessor = preprocessor
				,decode_error = decode_error
				,stop_words = stop_words
				,postprocessor = postprocessor
				,ngram_words = ngram_words
				
				,vocabulary = vocabulary
				,binary = binary
				,sparse = sparse
				,dtype = dtype
				,typecode = typecode
				,upper_limit = upper_limit
				
			)
		data.append(kwargs)
		pos += n
	
	pool = mp_pool or Pool(workers)
	v_partitions = pool.map(vectorize_part, data)
	return v_partitions
	
# ------------------------------------------------------------------------------

if __name__ == "__main__":
	from time import time
	import pandas as pd
	import numpy as np
	import pickle
	import marshal
	
	def my_preproc(text):
		return text.lower()
	
	test_re = re.compile(r'\ba\w{4,6}\b',re.U)
	def my_tokenizer(text):
		return test_re.findall(text)
	
	t0=time()
	lem_dict = marshal.load(open('lem_dict.mrl','rb'))
	print('lem_dict',int(time()-t0),'s')
	def my_postproc(tokens):
		out = []
		for t in tokens:
			lem = lem_dict.get(t)
			if not lem: continue
			out.append(lem)
		return out
	def my_postproc2(tokens):
		out = []
		for t in tokens:
			lem = lem_dict.get(t)
			if not lem: continue
			out.append(t)
		return out
	
	if 0:
		frame = pd.read_csv('flat/__all__.txt',sep='\t',header=None,names=['col','id','text'])
		t0=time()
		#df = get_df(frame.text,12,min_df=10,max_df=0.5)
		#dfy = get_dfy(frame.text,frame.col,workers=12,min_df=10,analyzer='char',ngram_range=(3,4))
		if 0:
			dfy = get_dfy(frame.text,frame.col,workers=12,min_df=10,postprocessor=my_postproc2)
			pickle.dump(dfy,open('nlp_dfy.pickle','wb'))
		else:
			dfy = pickle.load(open('nlp_dfy.pickle','rb'))
		for y in dfy:
			print(y,len(dfy[y]))
		print('dfy',time()-t0,'s')
		
		t0=time()
		topic = 'automaniak'
		
		if 0:
			df = get_df_from_dfy(dfy)
			chi = get_chi(df,len(frame.text),dfy[topic],Counter(frame.col)[topic])
			top_chi_words = [t for t,v in chi.most_common(100)]
			dfy = get_dfy(frame.text,frame.col,workers=12,min_df=10,ngram_range=(2,2),ngram_words=top_chi_words,stop_words=['a','i','o','w','z','u','na','do','lub'])
		
		df = get_df_from_dfy(dfy)
		for topic in [topic]:
			chi = get_chi(df,len(frame.text),dfy[topic],Counter(frame.col)[topic])
			chi_ex = get_chi_explain(df,len(frame.text),dfy[topic],Counter(frame.col)[topic])
			for t,v in chi.most_common(100):
				print(topic,t,v,df[t],dfy[topic][t])#,chi_ex[t])
		
		print('chi',time()-t0)
		print(len(df))
		
		t0=time()
		top_chi_words = [t for t,v in chi.most_common(100)]
		vectorized = vectorize(frame.text, vocabulary=top_chi_words,
			workers=12, postprocessor=my_postproc2,
			sparse=True, binary=False,
			typecode='H', dtype=None)
		print('vectorize',time()-t0)
		print(len(marshal.dumps(vectorized)))
		marshal.dump(vectorized,open('nlp_vectorized.marshal','wb'))
	else:
		t0=time()
		vectorized = marshal.load(open('nlp_vectorized.marshal','rb'))
		print('vectorize',time()-t0,'s')
	
	# print(min(df.values()))
	# for t,v in df.most_common(10):
		# print(t,v)
	
	# t0=time()
	# idf = get_idf(df,n,min_df=10)
	# for t,v in idf.most_common(10):
		# print(t,v,df[t])
	# print(time()-t0)
