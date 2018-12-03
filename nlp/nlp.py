"""
Functions for converting text documents into vector space
and dealing with dirty data.

Features:
- no external dependencies
- feature selection methods:
  - CHI
  - WCP (Within Class Probability)
  - CMFS (Comprehensively Measure Feature Selection)
  - improved GINI 
- CO matrix calcualtion
- DF calculation
- IDF calculation
"""

from multiprocessing import Pool
from collections import Counter
from itertools import groupby,chain
from math import log,ceil
import re

from batch import partitions as _partitions

# TODO resampling

# TODO przeniesienie feature selection do osobnego pliku
# TODO __init__.py

# TODO przyjecie nomenklatury t-term,c-category, tk, ci

# TODO reorder functions top-down vs bottom-up vs subject
# TODO smart lowercase (prosty NER w oparciu o DF[t] vs DF[t.lower])
# TODO sklearn model.fit/transform interface OR SIMILAR via functools.partial
# TODO liczenie lift dla co
# TODO wybieranie ngramow na podstawie liftu

# ---[ document frequency ]-----------------------------------------------------

def get_df_part(kwargs):
	min_df_part = kwargs['min_df_part']
	max_df_part = kwargs['max_df_part']
	min_tf_doc = kwargs['min_tf_doc']
		
	df = Counter()
	for tokens in iter_tokens_part(kwargs):
	
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

# TODO option to include whole words shorter than char ngram_range 'lo' value
# TODO option to mark word begin/end in char ngrams
# TODO max_df float
# TODO max_df int
# TODO max_df_part float
# TODO min_df float
# TODO reorder ARGS
def get_df(X, workers=4, as_dict=True, partitions=None,
		token_pattern='[\w][\w-]*', split_pattern='', encoding=None, 
		lowercase=True, min_df=0, min_df_part=0, max_df=1.0, max_df_part=1.0,
		analyzer='word', tokenizer=None, preprocessor=None,
		decode_error='strict', stop_words=None, mp_pool=None,
		min_tf_doc=0, ngram_range=None, postprocessor=None, ngram_words=None):
	"""Calculate document frequency from a collection of text documents.
	
	Parameters
	----------
	
	X : iterable
		Collection of text documents.
	
	workers : int, default=4
	
	partitions : int or None (default)
		Number of partitons. By default it will be equal to number of 
		workers
	
	token_pattern : string, default='[\w][\w-]*'
		Regular expression denoting what constitute a "token".
		Will not be used when tokenizer or split_pattern is defined.

	split_pattern : string, default=''
		Regular expression denoting what separetes "tokens".
		Will not be used when tokenizer is defined.
	
	ngram_range : tuple (lo, hi)
		The lower and upper "n" for n-grams to be extracted
	
	ngram_words: iterable or None (default)
		Limit n-gram generation to cases where at least one word occurs
		in the provided list.
	
	encoding: string or None (default)
	
	lowercase: boolean, default=True

	analyzer: str {'word','char'}
		Whether the features should be made of word or character n-grams.
		Option 'char' creates character n-grams only from text inside
		word boundaries.
	
	tokenizer: callable or None (default)
		Function which transforms text into list of tokens (before
		postprocessing and n-gram generation).
	
	preprocessor: callable, list of callable or None (default)
		Function or list of functions which transforms text before tokenization.

	postprocessor: callable, list of callable or None (default)
		Function(s) or list of functions which transforms list of tokens (before n-gram
		generation)

	min_df: int, default=0
	
	min_df_part: int, default=0
	
	min_tf_doc: int, default=0
	
	max_df: float, default=1.0
	
	max_df_part: float, default=1.0
	
	decode_error: str, default='strict'
	
	stop_words: iterable or None (default)
	
	mp_pool: multiprocessing.Pool or None (default)
		Multiprocessing pool object that will be used to parallelize
		execution. If none is provided a new one will be created.
	
	as_dict: boolean, default=True
		Whether the result should be converted into dict or left
		as collections.Counter (which doesn't support marshaling)
	"""
	data = []
	kwargs = dict(
			token_pattern = token_pattern
			,split_pattern = split_pattern
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
	part_cnt = partitions or workers
	if mp_pool and not partitions:
		part_cnt = max(part_cnt,len(mp_pool._pool))
	for lo,hi in _partitions(len(X),part_cnt):
		kw = dict(X=X[lo:hi], **kwargs)
		data.append(kw)
	
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
	if as_dict:
		df = dict(df)
	return df

### 24s get_dfy vs 11s get_df vs 25s get_dfy2(specialized)
def get_dfy(X,Y,workers=4,sort=True,mp_pool=None,**kwargs):
	"""Calcualte per topic document frequency.
	"""
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

def get_df_from_dfy(dfy,as_dict=True):
	"""Convert per topic document frequency into total document frequency.
	"""
	df = Counter()
	for y in dfy:
		df.update(dfy[y])
	if as_dict:
		df = dict(df)
	return df

# ---[ clean ]------------------------------------------------------------------

def limit_df(df,min_tokens=2,token_pattern='[\w][\w-]*', split_pattern='', tokenizer=None):
	"""function for limiting noise df to sentences with minimum number of tokens"""
	if token_pattern:
		re_tok = re.compile(token_pattern,re.U)
	if split_pattern:
		re_split = re.compile(split_pattern,re.U)
	new_df = {}
	for t in df:
		if tokenizer:
			tokens = tokenizer(t)
		elif split_pattern:
			tokens = re_split.split(t)
		elif token_pattern:
			tokens = re_tok.findall(t)
		if len(tokens)<min_tokens:
			continue
		new_df[t] = df[t]
	return new_df

# TODO replace based on matched split_pattern

def get_clean_x_part(kwargs):
	replace = kwargs['replace']
	out = []
	for tokens in iter_tokens_part(kwargs):
		out.append(replace.join(tokens))
	return out


# TODO refactor with get_df
def get_clean_x(X, workers=4, partitions=None,
		token_pattern='[\w][\w-]*', split_pattern='', encoding=None, 
		lowercase=True,
		tokenizer=None, preprocessor=None,
		decode_error='strict', stop_words=None, mp_pool=None,
		postprocessor=None,
		replace=u' ; ', stop_hashes=None, hash_fun=None):
	"""Replace noise tokens (words/phrases).
	
	Parameters
	----------
	
	X : iterable
		Collection of text documents.
	
	stop_words : iterable or None (default)
		Collection of tokens that should be replaced
	
	stop_hashes : iterable or None (default)
		Collection of hashes of tokens that should be replaced
	
	replace : str, default=u' ; '
		Replacement text for noise tokens
	
	workers : int, default=4
	
	token_pattern : string, default='[\w][\w-]*'
		Regular expression denoting what constitute a "token".
		Will not be used when tokenizer or split_pattern is defined.
	
	... TODO rest of params
	
	"""
	
	data = []
	part_cnt = partitions or workers
	if mp_pool and not partitions:
		part_cnt = max(part_cnt,len(mp_pool._pool))
	for lo,hi in _partitions(len(X),part_cnt):
		kwargs = dict(
				X = X[lo:hi]
				,token_pattern = token_pattern
				,split_pattern = split_pattern
				,encoding = encoding
				,lowercase = lowercase
				,tokenizer = tokenizer
				,preprocessor = preprocessor
				,decode_error = decode_error
				,stop_words = stop_words
				,postprocessor = postprocessor
				,replace = replace
				,stop_hashes = stop_hashes
				,hash_fun = hash_fun
			)
		data.append(kwargs)
	
	pool = mp_pool or Pool(workers)
	x_partitions = pool.map(get_clean_x_part, data)
	x=x_partitions[0]
	for x_ in x_partitions[1:]:
		x.extend(x_)
	return x

# ---[ feature selection ]------------------------------------------------------

def get_idf(df, n, a1=1, a2=1, a3=1, min_df=0):
	"""Calculate inverse document frequency.
	"""
	idf = Counter()
	for t in df:
		if min_df and df[t]<min_df: continue
		idf[t] = log( (a1+n) / (a2+df[t]) ) + a3
	return idf

# TODO mcd
def get_chiy(df,n,dfy,ny,alpha=0):
	chiy = {}
	for y in dfy:
		chiy[y] = get_chi(df,n,dfy[y],ny[y],alpha)
	return chiy
		
# TODO rename dfy,ny
def get_chi(df,n,dfy,ny,alpha=0):
	"""Calculate chi scores for features from one topic
	"""
	chi = {}
	for t,val in iter_chi(df,n,dfy,ny,alpha):
		chi[t] = val
	return chi

# TODO rename dfy,ny
def get_chi_explain(df,n,dfy,ny,alpha=0):
	chi_explain = iter_chi(df,n,dfy,ny,alpha,explain=True)
	return dict(chi_explain)

# TODO rename dfy,ny -> dfc (class), dft (topic)
# TODO rename chi variables
def iter_chi(df,n,dfy,ny,alpha=0,explain=False):
	all = df
	topic = dfy
	for t in df:
		# observed
		o_c1_t1 = topic.get(t,0)
		o_c1_t0 = ny - topic.get(t,0)
		o_c0_t1 = all[t] - topic.get(t,0)
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
		# result
		if explain:
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
			yield t,ex
		else:
			yield t,chi
			
# TODO gini(wcp) ???
def iter_wcpy(df,dfy,explain=False):
	topics = dfy.keys()
	V = len(df)
	for t in df:
		wcpy = {}
		py = {}
		for y in topics:
			nom =  1 + dfy[y].get(t,0)
			denom = V + df[t]
			py[y] = 1.0 * nom / denom
		sum_py = sum(py.values())
		for y in topics:
			wcpy[y] = py[y] / sum_py
		if explain:
			ex = dict()
			# TODO
			yield t,ex
		else:
			yield t,wcpy

def iter_giniy(df,dfy,ny,explain=False):
	topics = dfy.keys()
	for t in df:
		giniy = {}
		for y in topics:
			p_t_when_y = 1.0 * dfy[y].get(t,0) / ny[y]
			p_y_when_t = 1.0 * dfy[y].get(t,0) / df[t]
			giniy[y] = p_t_when_y**2 + p_y_when_t**2
		if explain:
			ex = dict()
			# TODO
			yield t,ex
		else:
			yield t,giniy


def iter_cmfsy(df,dfy,explain=False):
	topics = dfy.keys()
	C = len(topics)
	V = len(df)
	sum_dfy = {y:sum(dfy[y].values()) for y in topics}
		
	for t in df:
		cmfsy = {}
		for y in topics:
			nom = dfy[y].get(t,0) + 1
			denom1 = df[t] + C
			denom2 = sum_dfy[y] + V
			cmfsy[y] = 1.0 * nom / (denom1 * denom2)
		if explain:
			ex = dict()
			# TODO
			yield t,ex
		else:
			yield t,cmfsy

def get_giniy(df, dfy, ny):
	"""Calculate improved GINI for all topics
	"""
	items = iter_giniy(df,dfy,ny)
	topics = dfy.keys()
	return transform_items_topics(items, topics)

def get_cmfsy(df, dfy):
	"""
	http://www.dafl.yuntech.edu.tw/download/2012.IPM.48.A%20new%20feature%20selection%20based%20on%20comprehensive%20measurement%20both%20in%20inter-category%20and%20intra-category%20for%20text%20categorization.pdf
	"""
	items = iter_cmfsy(df,dfy)
	topics = dfy.keys()
	return transform_items_topics(items, topics)

def get_wcpy(df, dfy):
	"""Calculate WCP for all topics
	"""
	items = iter_wcpy(df, dfy)
	topics = dfy.keys()
	return transform_items_topics(items, topics)

# TODO opisac
def get_mcdy(fsy):
	"minimal class difference of feature score"
	topics = fsy.keys()
	mcdy = {y:{} for y in topics}
	vocab = set()
	for y in topics:
		vocab.update(fsy[y])
	for t in vocab:
		for y in topics:
			val = min([abs(fsy[y].get(t,0)-fsy[y2].get(t,0)) for y2 in topics if y!=y2])
			if val:
				mcdy[y][t] = val
	return mcdy


# ---[ vectorization ]----------------------------------------------------------

# TODO token_id iter not token_cnt

# TODO refactor using iter_tokens_part
def vectorize_part(kwargs):

	vocabulary = kwargs['vocabulary']
	binary = kwargs['binary']
	sparse = kwargs['sparse']
	stream = kwargs['stream']
	upper_limit = kwargs['upper_limit']
	
	dtype = kwargs['dtype']
	if dtype:
		import numpy as np
	typecode = kwargs['typecode']
	if typecode:
		from array import array

	if vocabulary==None:
		pass
	elif callable(vocabulary):
		pass
	elif hasattr(vocabulary,'items'):
		vocab_dict = vocabulary
		vocab_len = max(vocab_dict.values()) + 1
	else:
		vocab_dict = {t:t_id for t_id,t in enumerate(vocabulary)}
		vocab_len = len(vocabulary)

	out = []
	for tokens in iter_tokens_part(kwargs):
		# TODO filter tokens - keep only vocabulary -> here or after ngrams ???
				
		# output
		if stream:
			v = []
			if vocabulary==None:
				v.extend(tokens)
			elif callable(vocabulary):
				for t in tokens:
					v.append(vocabulary(t))
			else:
				empty = True # detection and removal of empty tokens combos
				for t in tokens:
					if t not in vocab_dict:
						continue # XXX
						if not empty:
							v.append(0) # XXX
						empty = True
						#continue # TODO optional -1 token
					else:
						t_id = vocab_dict[t]
						v.append(t_id)
						empty = False
			if dtype:
				v = np.array(v,dtype=dtype)
			if typecode:
				v = array(typecode,v)
		elif sparse:
			if binary:
				v = [vocab_dict[t] for t in set(tokens) if t in vocab_dict]
				if dtype:
					v = np.array(v,dtype=dtype)
				if typecode:
					v = array(typecode,v)
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
				if dtype:
					v = np.array(tf.items(),dtype=dtype)
				if typecode:
					pass # TODO
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
			if dtype:
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
def vectorize(X, vocabulary, workers=4, partitions=None,
	   token_pattern='[\w][\w-]*', split_pattern='',
	   encoding=None, lowercase=True,
	   analyzer='word', tokenizer=None, preprocessor=None,
	   decode_error='strict', stop_words=None, mp_pool=None,
	   ngram_range=None, ngram_words=None,
	   postprocessor=None, postprocessor2=None, 
	   binary=False, sparse=True, upper_limit=0,
	   dtype=None, typecode=None,
	   partitioned=False,
	   stream=False):
	"""Convert a collection of text documents into a collection of token counts
	
	Parameters
	----------
	
	X : iterable
	
	vocabulary : iterable or mapping or function
		TODO
	
	binary : boolean, default=False
		TODO
	
	sparse : boolean, default=True
		TODO
		
	stream : boolean, default=False
		TODO
	
	preprocessor: callable, list of callable or None (default)
		Function or list of functions which transforms text before tokenization.

	postprocessor: callable, list of callable or None (default)
		Function(s) or list of functions which transforms list of tokens (before n-gram
		generation)

	postprocessor2: callable, list of callable or None (default)
		Function(s) or list of functions which transforms list of tokens (after n-gram
		generation)
	
	upper_limit : int, default=0
		Upper limit for token counts in the vector
	
	dtype : numpy.dtype or None (default)
		numpy data type of the result
	
	typecode : str or None (default)
		array.array typecode of the result
	
	partitioned : boolean, default=False
		Whether the result should be partitioned or merged
		into a single list
	"""
	
	data = []
	part_cnt = partitions or workers
	if mp_pool and not partitions:
		part_cnt = max(part_cnt,len(mp_pool._pool))
	for lo,hi in _partitions(len(X),part_cnt):
		kwargs = dict(
				X = X[lo:hi]
				,token_pattern = token_pattern
				,split_pattern = split_pattern
				,encoding = encoding
				,lowercase = lowercase
				,analyzer = analyzer
				,ngram_range = ngram_range
				,tokenizer = tokenizer
				,preprocessor = preprocessor
				,decode_error = decode_error
				,stop_words = stop_words
				,postprocessor = postprocessor
				,postprocessor2 = postprocessor2
				,ngram_words = ngram_words
				
				,vocabulary = vocabulary
				,binary = binary
				,sparse = sparse
				,stream = stream
				,dtype = dtype
				,typecode = typecode
				,upper_limit = upper_limit
				
			)
		data.append(kwargs)
	
	pool = mp_pool or Pool(workers)
	v_partitions = pool.map(vectorize_part, data)
	
	if partitioned:
		out = v_partitions
	else:
		out = list(chain.from_iterable(v_partitions))
	return out

# ---[ cooccurrence ]-----------------------------------------------------------

# TODO parallelize


def get_co_part(kwargs):
	"""Calculate cooccurence count from a collection of token counts.
	"""

	X = kwargs['X']
	diagonal = kwargs['diagonal']
	triangular = kwargs['triangular']
	sparse = kwargs['sparse']
	binary = kwargs['binary']
	dtype = kwargs['dtype']
	stream = kwargs['stream']
	ngram_max = kwargs['ngram_max']
	symetry = kwargs['symetry']
	output_dtype = kwargs['output_dtype']
	upper_limit = kwargs['upper_limit']
	output_len = kwargs['output_len']
	min_df_part = kwargs['min_df_part']

	import numpy as np
	co = Counter()
	for x in X:
		if sparse:
			if binary:
				for t1 in x:
					for t2 in x:
						cnt = 1
						# TODO refactor
						if symetry:
							a = min(t1,t2)
							b = max(t1,t2)
						else:
							a = t1
							b = t2
						if a==b and not diagonal:
							continue
						co[a,b] += cnt
						if a!=b and not triangular and symetry:
							co[b,a] += cnt

			elif stream:
				for i in range(len(x)):
					t1 = x[i]
					if ngram_max:
						j_range = range(i,i+ngram_max)
					else:
						j_range = range(i,len(x))
					for j in j_range:
						if j>=len(x): break
						t2=x[j]
						if t2==0: break
						
						cnt = 1 
						# TODO refactor
						if symetry:
							a = min(t1,t2)
							b = max(t1,t2)
						else:
							a = t1
							b = t2
						if a==b and not diagonal:
							continue
						co[a,b] += cnt
						if a!=b and not triangular and symetry:
							co[b,a] += cnt
						
			else:
				if dtype:
					pass # TODO
				else:
					for t1 in x:
						for t2 in x:
							cnt = min(x[t1],x[t2])
							# TODO refactor
							if symetry:
								a = min(t1,t2)
								b = max(t1,t2)
							else:
								a = t1
								b = t2
							if a==b and not diagonal:
								continue
							co[a,b] += cnt
							if a!=b and not triangular and symetry:
								co[b,a] += cnt
		else:
			pass # TODO
	# limit within partition
	if min_df_part:
		below = [t for t in co if co[t]<min_df_part]
		for t in below:
			del co[t]
	if output_dtype and output_len:
		out = np.zeros((output_len,output_len),dtype=output_dtype)
		# for (t1,t2),f in co.items():
			# out[t1,t2] = min(upper_limit,f) if upper_limit else f
		if upper_limit:
			for (t1,t2),f in co.items():
				out[t1,t2] = min(upper_limit,f)
		else:
			for (t1,t2),f in co.items():
				out[t1,t2] = f
		return out
	else:
		return co

def get_co(X, workers=4, partitions=None, diagonal=True, triangular=False, sparse=True, binary=False,
		dtype=None,stream=False,ngram_max=None,symetry=True,
		output_dtype=None, upper_limit=0, output_len=None,
		mp_pool=None,as_dict=True,min_df_part=0):
	"""Calculate cooccurence count from a collection of token counts.
	"""
	import numpy as np

	if 1:
		kwargs = dict(
			diagonal=diagonal
			,triangular=triangular
			,sparse=sparse
			,binary=binary
			,dtype=dtype
			,stream=stream
			,ngram_max=ngram_max
			,symetry=symetry
			,output_dtype=output_dtype
			,upper_limit=upper_limit
			,output_len=output_len
			,min_df_part=min_df_part
		)
		pool = mp_pool or Pool(workers)
		# TODO refactor
		data = []
		part_cnt = partitions or workers
		if mp_pool and not partitions:
			part_cnt = max(part_cnt,len(mp_pool._pool))
		for lo,hi in _partitions(len(X),part_cnt):
			kw = dict(X=X[lo:hi],**kwargs)
			data.append(kw)
		
		co_parts = pool.map(get_co_part,data)
		# reduce
		if output_dtype:
			pass # TODO
		else:
			co = co_parts[0]
			for co_part in co_parts[1:]:
				co.update(co_part)
			
	else: # TODO remove this code
	
		co = Counter()
		for x in X:
			if sparse:
				if binary:
					for t1 in x:
						for t2 in x:
							cnt = 1
							# TODO refactor
							if symetry:
								a = min(t1,t2)
								b = max(t1,t2)
							else:
								a = t1
								b = t2
							if a==b and not diagonal:
								continue
							co[a,b] += cnt
							if a!=b and not triangular and symetry:
								co[b,a] += cnt

				elif stream:
					for i in range(len(x)):
						t1 = x[i]
						if ngram_max:
							j_range = range(i,i+ngram_max)
						else:
							j_range = range(i,len(x))
						for j in j_range:
							if j>=len(x): break
							t2=x[j]
							if t2==0: break
							
							cnt = 1 
							# TODO refactor
							if symetry:
								a = min(t1,t2)
								b = max(t1,t2)
							else:
								a = t1
								b = t2
							if a==b and not diagonal:
								continue
							co[a,b] += cnt
							if a!=b and not triangular and symetry:
								co[b,a] += cnt
							
				else:
					if dtype:
						pass # TODO
					else:
						for t1 in x:
							for t2 in x:
								cnt = min(x[t1],x[t2])
								# TODO refactor
								if symetry:
									a = min(t1,t2)
									b = max(t1,t2)
								else:
									a = t1
									b = t2
								if a==b and not diagonal:
									continue
								co[a,b] += cnt
								if a!=b and not triangular and symetry:
									co[b,a] += cnt
			else:
				pass # TODO
	
	if output_dtype and output_len:
		out = np.zeros((output_len,output_len),dtype=output_dtype)
		# for (t1,t2),f in co.items():
			# out[t1,t2] = min(upper_limit,f) if upper_limit else f
		if upper_limit:
			for (t1,t2),f in co.items():
				out[t1,t2] = min(upper_limit,f)
		else:
			for (t1,t2),f in co.items():
				out[t1,t2] = f
		return out
	else:
		return dict(co) if as_dict else co

def get_coy(X,Y,sort=True,**kwargs):
	"""Calculate per topic cooccurence count from a collection of token counts.
	"""
	coy = {}
	if sort:
		data = sorted(zip(Y,X))
	else:
		data = zip(Y,X)
	for y,g in groupby(data,lambda x:x[0]):
		x = [v[1] for v in g]
		coy[y] = get_co(x,**kwargs)
	return coy

# TODO np.array input
def get_co_from_coy(coy,dtype=None):
	"""Convert per topic cooccurence count into total cooccurence count.
	"""
	if dtype:
		import numpy as np
		co = np.zeros_like(list(coy.values())[0],dtype=dtype)
		for y in coy:
			co += coy[y]
	else:
		co = Counter()
		for y in coy:
			co.update(coy[y])
	return co

# ---[ tokens ]-----------------------------------------------------------------

def iter_tokens_part(kwargs):
	X = kwargs['X']
	token_pattern = kwargs['token_pattern']
	split_pattern = kwargs['split_pattern']
	stop_words = kwargs['stop_words']
	lowercase = kwargs['lowercase']
	encoding = kwargs['encoding']
	decode_error = kwargs['decode_error']
	preprocessor = kwargs['preprocessor']
	tokenizer = kwargs['tokenizer']
	postprocessor = kwargs['postprocessor']
	postprocessor2 = kwargs.get('postprocessor2')
	
	ngram_range = kwargs.get('ngram_range')
	ngram_words = kwargs.get('ngram_words')
	analyzer = kwargs.get('analyzer') or 'word'

	stop_hashes = kwargs.get('stop_hashes')
	hash_fun = kwargs.get('hash_fun') or hash
	
	stop_words_set = set(stop_words or [])
	stop_hashes_set = set(stop_hashes or [])
	
	ngram_words_set = set(ngram_words or [])
	
	if token_pattern:
		re_tok = re.compile(token_pattern,re.U)
	if split_pattern:
		re_split = re.compile(split_pattern,re.U)
	out = []
	for text in X:
		if encoding:
			text = text.decode(encoding,decode_error)
		if preprocessor:
			if callable(preprocessor):
				text = preprocessor(text)
			else:
				for p in preprocessor:
					text = p(text)
		if lowercase:
			text = text.lower()
		if tokenizer:
			tokens = tokenizer(text)
		elif split_pattern:
			tokens = re_split.split(text)
		elif token_pattern:
			tokens = re_tok.findall(text)
		if postprocessor:
			if callable(postprocessor):
				tokens = postprocessor(tokens)
			else:
				for p in postprocessor:
					tokens = p(tokens)
		if stop_words:
			tokens = [t for t in tokens if t not in stop_words_set]
		if stop_hashes:
			tokens = [t for t in tokens if hash_fun(t) not in stop_hashes_set]
		
		if ngram_range:
			lo,hi = ngram_range
			ngrams = []
			if analyzer=='word':
				for i in range(len(tokens)-lo+1):
					for n in range(lo,hi+1):
						if i+n>len(tokens): break
						ngram = tuple(tokens[i:i+n])
						if ngram_words_set and not ngram_words_set&set(ngram): continue
						ngrams.append(ngram) # ngram as tuple is easier to postprocess
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

		if postprocessor2:
			if callable(postprocessor2):
				tokens = postprocessor2(tokens)
			else:
				for p in postprocessor2:
					tokens = p(tokens)

		yield tokens


# ---[ utils ]------------------------------------------------------------------

def transform_items_topics(items, topics):
	"transforms items of dict[token][topic]->val into dict[topic][token]->val dictionary"
	out = {y:{} for y in topics}
	for t,d in items:
		for y in topics:
			val = d[y]
			if val:
				out[y][t] = val
	return out
