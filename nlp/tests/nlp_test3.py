import sys; sys.path.append('..')

from time import time
from nlp import *
from frame import *
from tsv import *
from cache import *

if __name__=="__main__":
	cache = disk_cache('../cache','v2',show_time=True)
	
	# frame
	t0=time()
	rows = tsv_iter('../data/__all__.txt')
	frame = frame_from_iter(rows,['col','id','text'])
	print('frame {:.2f} s'.format(time()-t0))

	# dfy
	dfy = cache.use('dfy2', get_dfy, frame['text'], frame['col'], min_df=10)
	
	# df
	df = cache.use('df', get_df_from_dfy, dfy)
	
	# chi
	topic = 'automaniak'
	chi = cache.use('chi_'+topic, get_chi, df, len(frame['text']), dfy[topic], Counter(frame['col'])[topic], as_dict=True)

	for t,v in Counter(chi).most_common(100):
		print(topic,t,v)

