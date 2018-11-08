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
	cache = disk_cache('../cache','t5v2',verbose=True,linear=True)
	
	pool = Pool(4,load_lem_dict)

	# frame
	t0=time()
	rows = tsv_iter('../data/__all__.txt')
	frame = frame_from_iter(rows, ['col', 'id', 'text'])
	print('frame\t{:.2f} s'.format(time()-t0))
	print('frame\t{} rows'.format(len(frame['id'])))
	
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
		postprocessor=lem_only,
		min_df=10,
		mp_pool=pool)
	
	# df
	df = get_df_from_dfy(dfy)
	
	# chiy
	chiy = cache.use('chiy', get_chiy, df, len(X), dfy, Counter(frame['col']))
	
	# wcpy
	wcpy = cache.use('wcpy', get_wcpy, df, dfy)
	
	# vocaby
	vocaby = {}
	for y in chiy:
		t_v = Counter(chiy[y]).most_common(200)
		#t_v = Counter(wcpy[y]).most_common(20)
		vocaby[y] = set([t for t,v in t_v])
		#print(y,vocaby[y])
	
	#cache.missed = True
	
	# vocab
	vocab = set()
	for y in vocaby:
		vocab.update(vocaby[y])
	print('len_vocab',len(vocab))

	# term_id
	term_id = {t:i for i,t in enumerate(vocab)}

	# vec_vocaby
	vec_vocaby = {}
	for y in vocaby:
		vec_vocaby[y] = set([term_id[t] for t in vocaby[y]])
	
	# vectorized
	V = cache.use('vectorized',
		#vectorize, X, vocab,
		vectorize, frame['text'], vocab,
		#preprocessor=[replace_numbers,replace_links],
		postprocessor=lem_only,
		mp_pool=pool)
	
	frame['tf'] = V

	# col_score & all_score
	t0 = time()
	col_score = []
	all_score = []
	for col,tf in zip(frame['col'],frame['tf']):
		common = set(tf) & vec_vocaby[col]
		col_score.append(len(common))
		all_score.append(len(tf))
	frame['col_score'] = col_score
	frame['all_score'] = all_score
	print('col_score\t{:.2f} s'.format(time()-t0))

	# low score examples
	topic='kibic'
	for col,als,cls,text in zip(frame['col'],frame['all_score'],frame['col_score'],frame['text']):
		if col==topic and cls==0:
			pass
			#print(col,als,cls,text)

	# score vocab
	cs_zero = Counter()
	as_zero = Counter()
	all = Counter()
	for col,cs,as_ in zip(frame['col'],frame['col_score'],frame['all_score']):
		all[col] += 1
		if cs==0:
			cs_zero[col] += 1
		if as_==0:
			as_zero[col] += 1
	for col in sorted(all):
		x = 1.0 * cs_zero[col]/all[col]
		print(col,x,as_zero[col],cs_zero[col],all[col])
		
	total_cs_zero = sum(cs_zero.values())
	total_as_zero = sum(as_zero.values())
	total_all = sum(all.values())
	x = 1.0 * total_cs_zero / total_all
	print('TOTAL',x,total_as_zero,total_cs_zero,total_all)
	
	# export
	t0 = time()
	if 1:
		feature_cnt = len(vocab)
		with open('../data/vectorized.tsv','wb',100000) as fo:
			for row in iter_from_frame(frame,['col','id','col_score','tf']):
				if row[-2]==0: continue # omit col_score==0
				tf = row[-1]
				features = [str(tf.get(j,0)) for j in range(feature_cnt)]
				fo.write(row[0]+'\t')
				fo.write(row[1]+'\t')
				fo.write('\t'.join(features))
				fo.write('\n')
	elif 0:
		args = []
		feature_cnt = len(vocab)
		for p,(lo,hi) in enumerate(partitions(len(frame['id']),4)):
			f = {}
			f['col'] = frame['col']
			f['id'] = frame['id']
			args += [(p,lo,hi,feature_cnt,f,V)]
		pool.map(export_part,args)
	print('export',time()-t0)
