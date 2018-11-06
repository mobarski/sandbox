import sys; sys.path.append('..')

from time import time
import re

from nlp import *
from frame import *
from tsv import *
from cache import *

from multiprocessing import Pool

if 1:
	# dict
	def load_lem_dict():
		global lem_dict
		t0=time()
		lem_dict = marshal.load(open('../data/lem_dict.mrl','rb'))
		#print('lem_dict {:.2f} s'.format(time()-t0))
	
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


def export_part(args):
	p,lo,hi,feature_cnt,frame,V = args
	with open('../data/vectorized_{}.tsv'.format(p),'wb',100000) as fo:
		for i in range(lo,hi):
			fo.write(frame['col'][i])
			fo.write('\t')
			fo.write(frame['id'][i])
			fo.write('\t')
			
			vi = V[i]
			v = [str(vi.get(j,0)) for j in range(feature_cnt)]
			fo.write('\t'.join(v))
			fo.write('\n')

re_num = re.compile(r'\b\d+\b')
def replace_numbers(text):
	return re_num.sub('_NUM_',text)

re_link = re.compile(r'>>>>[^<]*<<<<')
def replace_links(text):
	return re_link.sub('_LINK_',text)

if __name__=="__main__":
	cache = disk_cache('../cache','t5v2',show_time=True,linear=True)
	
	pool = Pool(4,load_lem_dict)

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
	
	# dfy
	dfy = cache.use('dfy', get_dfy,
		X, frame['col'],
		postprocessor=in_dict_only,
		min_df=10,
		mp_pool=pool)
	
	# df
	df = cache.use('df', get_df_from_dfy, dfy)
	
	# chi
	chiy = cache.use('chiy', get_chiy, df, len(X), dfy, Counter(frame['col']))
	
	# vocabulary
	vocab = set()
	for y in chiy:
		t_v = Counter(chiy[y]).most_common(100)
		vocab.update([t for t,v in t_v])
	print('len_vocab',len(vocab))

	# vectorized
	V = cache.use('vectorized',
		vectorize, X, vocab,
		postprocessor=in_dict_only,
		mp_pool=pool)

	# export
	t0 = time()
	if 0:
		with open('../data/vectorized_{}.tsv'.format(p),'wb',100000) as fo:
			row_cnt = len(frame['id'])
			feature_cnt = len(vocab)
			for i in range(row_cnt):
				fo.write(frame['col'][i])
				fo.write('\t')
				fo.write(frame['id'][i])
				fo.write('\t')
				
				vi = V[i]
				v = [str(vi.get(j,0)) for j in range(feature_cnt)]
				fo.write('\t'.join(v))
				fo.write('\n')

	args = []
	feature_cnt = len(vocab)
	for p,(lo,hi) in enumerate(partitions(len(frame['id']),4)):
		f = {}
		f['col'] = frame['col']
		f['id'] = frame['id']
		args += [(p,lo,hi,feature_cnt,f,V)]
	pool.map(export_part,args)
	print('export',time()-t0)
