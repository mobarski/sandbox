# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ---[ DATA ]-------------------------------------------------------------------

"""Access data from json files as documents (paragraph level dicts)"""

# ---[ list ]-------------------------------------------------------------------

import os

def list_data_files():
	"""iterate over paths of all data files"""
	for dirpath,_,filenames in os.walk('data'):
		filenames = [f for f in filenames if f.endswith('.json')]
		if not filenames: continue
		for f in filenames:
			yield os.path.join(dirpath,f)

# ---[ convert ]----------------------------------------------------------------

import json

def json_to_docs(path):
	"""iterate over paragraph level documents from one json document"""
	paper = json.load(open(path,'rb'))
	# parts
	text_id = 0
	for part in ['abstract','body_text']:
		if part not in paper: continue
		for x in paper[part]:
			doc = {}
			# metadata
			doc['paper_id'] = paper['paper_id']
			doc['paper_title'] = paper['metadata']['title']
			doc['path'] = path
			doc['part'] = part
			text_id += 1
			doc['text_id'] = text_id
			#
			doc['text'] = x['text']
			doc['section'] = x['section']
			# bib
			doc['bib_titles'] = []
			for ref in x['cite_spans']:
				ref_id = ref['ref_id']
				if not ref_id: continue 
				ref_title = paper['bib_entries'][ref_id]['title'] # ERROR
				doc['bib_titles'] += [ref_title]
			# ref (tables and figures)
			doc['tables'] = []
			doc['figures'] = []
			for ref in x['ref_spans']:
				ref_id = ref['ref_id']
				if not ref_id: continue
				r = paper['ref_entries'][ref_id] # ERROR
				if r['type']=='table':
					doc['tables'] += [r['text']]
				if r['type']=='figure':
					doc['figures'] += [r['text']]
			yield doc

def doc_iter(limit=None):
	"""iterate over all documents (doc = single paragraph)"""
	from itertools import islice
	for path in islice(list_data_files(),limit):
		yield from json_to_docs(path)

def get_doc(path,text_id):
	"""get single document (paragraph)"""
	docs = json_to_docs(path)
	for doc in docs:
		if doc['text_id']==text_id:
			return doc

def get_doc_by_meta(meta):
	path = meta['path']
	text_id = meta['text_id']
	return get_doc(path,text_id)

# ------------------------------------------------------------------------------

import numpy as np
import re

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
	m = {f:doc[f] for f in ['paper_id','text_id','path']}
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

split_tokens_re = re.compile('[\s.,;!?()\[\]]+')
upper_re = re.compile('[A-Z]')
num_re = re.compile('\d+|\d+[%]|\d+[a-z]|[#]\d+|[~]\d+')
url_re = re.compile('[hH][tT][tT][pP][sS]?://[a-zA-Z._0-9/=&?,|%-]+')
dna_re = re.compile('[AGCT]{8,}')

def text_to_tokens(text):
	text = url_re.sub('<URL>',text)
	tokens = split_tokens_re.split(text)
	tokens = [t.lower() if len(t)>1 and len(upper_re.findall(t))<2 else t for t in tokens]
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
	limit = None
	workers = 34
	label = limit or 'all'
	model = inverness.Model(f'model_{label}_v7/')
	# functions
	#
	if 0:
		model.load(['fun','meta','phraser','dictionary','tfidf','lsi','dense_ann'])
	else:
		model.text_to_tokens = text_to_tokens
		model.doc_to_text = doc_to_text
		model.get_doc_by_meta = get_doc_by_meta
		model.doc_iter = lambda:doc_iter(limit)
		model.get_meta = get_meta
		model.init_fun()
		#
		model.init_meta(storage='disk')
		exit()
		model.skip_phraser()
		model.skip_phrased()
		model.init_dictionary()
		model.prune_dictionary(**prune_cfg)
		#print('dfs[0]:',model.dictionary.dfs[0])
		model.init_bow(storage='disk')
		#print('bow[0]:',model.bow[0])
		model.phrased.delete() # del
		#model.init_inverted()
		model.init_tfidf(**tfidf_cfg)
		if workers>1:
			model.init_sparse_mp(workers)
		else:
			model.init_sparse(storage='disk')
		print('sparse[0]:',model.sparse[0])
		model.bow.delete() # del
		model.init_lsi(**lsi_cfg)
		if workers>1:
			model.init_dense_mp(workers)
		else:
			model.init_dense(storage='disk')
		model.sparse.delete() # del
		model.init_dense_ann(post=2)
		model.dense.delete() # del

	print(f'\n\ntotal: {time()-t0:.01f}s\n\n')


	# ------------------------------------------------------------------------------
	# ------------------------------------------------------------------------------
	# ------------------------------------------------------------------------------

	def test_model(ids,fun,k=1):
		ok_cnt = 0
		for i in ids:
			m = model.meta[i]
			query = model.doc_to_text(model.doc_to_text(model.get_doc_by_meta(m)))
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
	