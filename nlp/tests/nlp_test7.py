import sys; sys.path.append('..')

from time import time
import re

from nlp import *
from frame import *
from tsv import *
from cache import *

from multiprocessing import Pool

"""
test #7 - vectorization with complete vocabulary
"""

if __name__=="__main__":
	cache = disk_cache('../cache/test7',verbose=True,linear=True)
	pool = Pool(4)

	# frame
	t0=time()
	rows = tsv_iter('../data/__all__.txt')
	frame = frame_from_iter(rows, ['col', 'id', 'url', 'text'])
	print('frame\t{:.2f} s'.format(time()-t0))
	print('frame\t{} rows'.format(len(frame['id'])))

	X = frame['text']
	
	# df
	df = cache.set('df', get_df,
		X,
		partitions=24,min_df_part=2,
		postprocessor=None,
		min_df=2, # 10:150k 5:235k 2:490k
		mp_pool=pool)
	exit()

	# vocab
	vocab = list(sorted(df))	
	cache.set('vocab',vocab)

	# vector
	V = cache.set('vector',
		vectorize, X, vocab,
		binary=True,dtype='l',
		mp_pool=pool)
