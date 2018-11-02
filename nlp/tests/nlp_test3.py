import sys; sys.path.append('..')

from time import time
from nlp import *
from frame import *
from tsv import *
from cache import *

if __name__=="__main__":
	cache = disk_cache('../cache','v2')
	
	# frame
	t0=time()
	rows = tsv_iter('../data/__all__.txt')
	frame = frame_from_iter(rows,['col','id','text'])
	print('frame {:.2f} s'.format(time()-t0))

	# dfy
	t0=time()
	dfy = cache.use('dfy2', get_dfy, frame['text'], frame['col'], min_df=10)
	print('dfy {:.2f} s'.format(time()-t0))
	
	# df
	t0=time()
	df = get_df_from_dfy(dfy)
	print('df {:.2f} s'.format(time()-t0))
	
	# chi
	t0=time()
	topic = 'automaniak'
	chi = get_chi(df, len(frame['text']), dfy[topic], Counter(frame['col'])[topic])
	print('chi {:.2f} s'.format(time()-t0))
	
	for t,v in chi.most_common(100):
		print(topic,t,v)
	