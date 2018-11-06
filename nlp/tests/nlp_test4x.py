import sys; sys.path.append('..')

from time import time
import re

from nlp import *
from frame import *
from tsv import *
from cache import *

from multiprocessing import Pool


def load_lem_dict():
	global lem_dict
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

re_num = re.compile(r'\b\d+\b')
def replace_numbers(text):
	return re_num.sub('_NUM_',text)

re_link = re.compile(r'>>>>[^<]*<<<<')
def replace_links(text):
	return re_link.sub('_LINK_',text)


if __name__=="__main__":
	cache = disk_cache('../cache','t4v1',show_time=True,linear=True)
	
	topic = 'alergie'
	load_lem_dict()
	
	#pool = Pool(4,load_lem_dict)

	# frame
	t0=time()
	rows = tsv_iter('../data/__all__.txt')
	frame = frame_from_iter(rows, ['col', 'id', 'text'])
	print('frame {:.2f} s'.format(time()-t0))
	
	# noise
	# TODO test split with also "..."
	noise = cache.use('noise', get_df,
		frame['text'],
		split_pattern='[\s;]*[;.][\s;]*',
		preprocessor=[replace_numbers,replace_links], postprocessor=None,
		min_df_part=2, min_df=2)
	
	# clean_x
	X = cache.use('clean_x',get_clean_x,
		frame['text'],
		split_pattern='[\s;]*[;.][\s;]*',
		preprocessor=[replace_numbers,replace_links], postprocessor=None,
		replace=u' ; ', stop_words=noise)
	
	# dump clean_x[topic ]
	xa = [x for x,c in zip(X,frame['col']) if c==topic]
	f = open('xa.txt','wb')
	for x in xa:
		f.write(x.encode('utf8'))
		f.write('\n')
	
	# dfy
	dfy = cache.set('dfy', get_dfy,
		X, frame['col'],
		postprocessor=in_dict_only,
		min_df=10)
	
	# df
	df = cache.use('df', get_df_from_dfy, dfy)
	
	# chi
	chi = cache.use('chi_'+topic, get_chi, df, len(X), dfy[topic], Counter(frame['col'])[topic])
	
	# vocabulary
	vocab = Counter(chi).most_common(100)
	for t,v in vocab:
		print(topic,t,v)
		pass
	vocab = [t for t,v in vocab]

	# vectorized
	V = cache.use('vectorized', vectorize, X, vocab)

	# check
	topic_cnt = Counter(frame['col'])
	#cnt_by_topic = zip(frame['col'],[len(v) for part in V for v in part])
	cnt_by_topic = zip(frame['col'],[len(v) for v in V])
	cnt = Counter()
	for t,c in cnt_by_topic:
		cnt[t] += c
	for t in cnt:
		print t,int(1.0*cnt[t]/topic_cnt[t]),cnt[t],topic_cnt[t]


