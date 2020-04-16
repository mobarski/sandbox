import numpy as np
import re

sentencer_cfg = {'no_matching' : re.compile(
		'(?i)All rights reserved'+
		'|No reuse allowed'+
		'|author/funder'+
		'|this preprint'
	)
}

phraser_cfg = {
	'min_count' : 3,
	'threshold' : 1.0,
	'delimiter' : b'__',
	'components' : True,
	'common_terms' : [
		'','to','and','of','the','a','an','in','by','for','on','that','or',
		'was','this','then','than','is','with','/','*','+','-','=','<','>',
		'could','be','here','we','has','are','there','as','did','not',
		'from','may','have','from','our','et','al','under','were','these',
		'at','out','but','also','it','into','de','one','two','had','no','not','so'
	],
}

prune_cfg = {
	'no_below': 2,
	'no_above': 0.50,
	'keep_tokens': ['<PAD>','<DNA>'],
	'stopwords': [],
}

tfidf_cfg = {'smartirs':'ltu'}

lsi_cfg = {
	'num_topics': 100,
	'dtype': np.single,
	'onepass': False,
}

def get_meta(id,doc):
	m = {f:doc[f] for f in ['paper_id','text_id','paper_title','path']}
	m['id'] = id # DEBUG
	return m

def doc_to_text(doc):
	values = [
			doc['text'],
			doc['section'],
			'\n'.join(doc['tables']),
			'\n'.join(doc['figures']),
			'\n'.join(doc['bib_titles'])
		]
	return '\n'.join(values)

# ------------------------------------------------------------------------------

split_sentences_re = re.compile('(?<!.prof|et al|. [Ff]ig)[.?!;]+(?: (?=[A-Z\n])|\n)')
split_tokens_re = re.compile('[\s.,;!?()\[\]]+')
upper_re = re.compile('[A-Z]')

num_re = re.compile('\d+|\d+[%]|\d+[a-z]|[#]\d+|[~]\d+')
url_re = re.compile('[hH][tT][tT][pP][sS]?://[a-zA-Z._0-9/=&?,|%-]+')
dna_re = re.compile('[AGCT]{8,}')

def text_to_sentences(text):
	return [s.strip() for s in split_sentences_re.split(text) if s.strip()]

def text_to_tokens(text):
	text = url_re.sub('<URL>',text)
	tokens = split_tokens_re.split(text)
	tokens = [t.lower() if len(t)>1 and len(upper_re.findall(t))<2 else t for t in tokens]
	#tokens = [t.lower() for t in tokens]
	tokens = ['<NUM>' if num_re.match(t) else t for t in tokens]
	tokens = ['<DNA>' if dna_re.match(t) else t for t in tokens]
	return tokens

# ------------------------------------------------------------------------------
if __name__=="__main__":
	from pprint import pprint
	from itertools import islice
	from time import time
	t0 = time()
	import inverness
	import data
	limit = 1000
	workers = 1 # 1->155s 2->154s 4->169s
	label = limit or 'all'
	model = inverness.Model(f'model_{label}/')
	# functions
	#
	if 1:
		model.text_to_sentences = text_to_sentences
		model.text_to_tokens = text_to_tokens
		model.doc_to_text = doc_to_text
		model.get_doc_by_meta = data.get_doc_by_meta
		model.doc_iter = lambda:data.doc_iter(limit)
		model.get_meta = get_meta
		model.init_fun()
		#
		model.init_meta()
		if 1: # 155s
			model.skip_phraser()
			model.skip_phrased()
		else: # 263s
			#model.init_sentencer(**sentencer_cfg)
			model.skip_sentencer()
			model.init_phraser(**phraser_cfg)
			if workers>1:
				model.init_phrased_mp(workers)
			else:
				model.init_phrased()
			print('phrased[0]:',model.phrased[0])
		model.init_dictionary(save=True)
		model.prune_dictionary(**prune_cfg)
		print('dfs[0]:',model.dictionary.dfs[0])
		model.init_bow()
		print('bow[0]:',model.bow[0])
		#model.phrased.delete() # del
		#model.init_inverted()
		model.init_tfidf(**tfidf_cfg)
		if workers>1:
			model.init_sparse_mp(workers)
		else:
			model.init_sparse()
		print('sparse[0]:',model.sparse[0])
		#model.bow.delete() # del
		model.init_lsi(**lsi_cfg)
		if workers>1:
			model.init_dense_mp(workers)
		else:
			model.init_dense()
		model.init_dense_ann(post=2)
		#model.dense.delete() # del
		#model.init_sparse_ann(post=2)
		#model.sparse.delete() # del
	else:
		model.load_meta()
		model.load_sentencer()
		#model.load_phraser()
		model.skip_phraser()
		model.load_phrased()
		model.load_dictionary()
		model.load_inverted()
		model.load_tfidf()
		model.load_lsi()
		model.load_sparse()
		model.load_dense()
		model.load_sparse_ann()
		model.load_dense_ann()

	print(f'\n\ntotal: {time()-t0:.01f}s\n\n')


	# ------------------------------------------------------------------------------
	# ------------------------------------------------------------------------------
	# ------------------------------------------------------------------------------

	def test_model(ids,fun,k=1):
		ok_cnt = 0
		for i in ids:
			m = model.meta[i]
			query = model.doc_to_text(data.get_doc(m['path'],m['text_id']))
			top = list(fun(query))[:k] # id,score,m
			top_ids = [x[0] for x in top]
			if i in top_ids:
				ok_cnt += 1
		return ok_cnt / len(ids)

	N = 1000
	from random import randint
	ids = [randint(0,len(model.meta)-1) for _ in range(N)]
	#print('sparse score:',test_model(ids, model.find_sparse))
	print('dense score: ',test_model(ids, model.find_dense))
	