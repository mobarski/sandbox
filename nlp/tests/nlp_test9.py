import sys; sys.path.append('..')

from time import time
import re

from nlp import *
from frame import *
from tsv import *
from cache import *

from multiprocessing import Pool

"""
test #8 - ngram words
"""

if __name__=="__main__":
	cache = disk_cache('../cache/v6',verbose=True,linear=True)
	pool = Pool(4)

	# frame
	t0=time()

	X = cache.get('clean_x')
	Y = cache.get('col')
	df = cache.get('df')
	
	chiy = cache.get('chiy')
	vocab = set()
	for y in chiy:
		top = [x[0] for x in Counter(chiy[y]).most_common(100)]
		vocab.update(top)
	stop_words = [t for t,f in Counter(df).most_common(100)] + ['_link_','+num_']
	
	# dfy
	dfy = cache.set('dfy_n22', get_dfy,
		X,Y,min_df_part=10,
		postprocessor=None,
		ngram_words=vocab,
		stop_words=stop_words,
		ngram_range=(2,2),
		mp_pool=pool)
	for y in dfy:
		print(y,Counter(dfy[y]).most_common(20))
