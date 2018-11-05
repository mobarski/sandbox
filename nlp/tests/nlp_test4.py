import sys; sys.path.append('..')

from time import time
import re

from nlp import *
from frame import *
from tsv import *
from cache import *

if 0:
	t0=time()
	lem_dict = marshal.load(open('../data/lem_dict.mrl','rb'))
	print('lem_dict {:.2f} s'.format(time()-t0))
	def lem_only(tokens):
		out = []
		for t in tokens:
			lem = lem_dict.get(t)
			if not lem: continue
			out.append(lem)
		return out
	def in_dict_only(tokens):
		out = []
		for t in tokens:
			lem = lem_dict.get(t)
			if not lem: continue
			out.append(t)
		return out

if __name__=="__main__":
	cache = disk_cache('../cache','t4v1',show_time=True,linear=True)
	
	# frame
	t0=time()
	rows = tsv_iter('../data/__all__.txt')
	frame = frame_from_iter(rows, ['col', 'id', 'text'])
	print('frame {:.2f} s'.format(time()-t0))
	
	# noise
	noise = cache.use('noise', get_df,
		frame['text'], split_pattern='[\s;]*;[\s;]*',
		min_df_part=2, min_df=2)
	
	# clean_x
	X = cache.use('clean_x',get_clean_x,
		frame['text'], split_pattern='[\s;]*;[\s;]*', replace=u' ; ',
		stop_words=noise)

	# dfy
	dfy = cache.use('dfy', get_dfy,
		X, frame['col'], postprocessor=None, min_df=10)
	
	# df
	df = cache.use('df', get_df_from_dfy, dfy)
	
	# chi
	topic = 'planszomaniak'
	chi = cache.use('chi_'+topic, get_chi, df, len(X), dfy[topic], Counter(frame['col'])[topic])
	
	# vocabulary
	vocab = Counter(chi).most_common(200)
	for t,v in vocab:
		print(topic,t,v)
	vocab = [t for t,v in vocab]

	# vectorized
	V = cache.use('vectorized', vectorize, X, vocab)

	print(V)
	