import pandas as pd
from collections import Counter
import re

from multiprocessing import Pool
from time import time

df = pd.read_csv('flat/__all__.txt',sep='\t',header=None,names=['col','id','text'])

def tf_df_part(args):
	iterable, token_pattern, encoding = args
	re_tok = re.compile(token_pattern,re.U)
	tf = Counter()
	df = Counter()
	for text in iterable:
		text = text.decode(encoding).lower() # TODO lowercase arg
		tokens = re_tok.findall(text)
		tf.update(tokens)
		df.update(set(tokens))
	return tf,df

# TODO strip_accents
# TODO decode_error
# TODO lematize
# TODO stop_words
# TODO ngram_range + analyzer (word,char)
def get_tf_df(iterable, workers=4, token_pattern='[\w][\w-]*', encoding='utf8'):
	cnt = len(iterable)
	
	data = []
	n = cnt/workers # TEST
	x = 0
	for i in range(workers):
		lo = x
		hi = min(cnt-1,lo+n)
		data.append([iterable[lo:hi],token_pattern,encoding])
		x += n
	
	pool = Pool(workers)
	tf_df = pool.map(tf_df_part, data)
	tf,df=tf_df[0]
	for tf_,df_ in tf_df[1:]:
		tf.update(tf_)
		df.update(df_)
	
	return tf,df

t0=time()
tf,df = get_tf_df(df.text,12)
print(time()-t0)
