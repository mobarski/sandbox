import numpy as np

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
	'no_above': 0.05,
	'keep_tokens': ['<PAD>'],
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

import re
split_sentences_re = re.compile('(?<!.prof|et al|. [Ff]ig)[.?!;]+(?: (?=[A-Z\n])|\n)')
split_tokens_re = re.compile('[\s.,;!?()\[\]]+')
upper_re = re.compile('[A-Z]')

num_re = re.compile('\d+|\d+[%]|\d+[a-z]|[#]\d+|[~]\d+')
url_re = re.compile('[hH][tT][tT][pP][sS]?://[a-zA-Z._0-9/=&?,|%-]+')

def text_to_sentences(text):
	return [s.strip() for s in split_sentences_re.split(text) if s.strip()]

def text_to_tokens(text):
	text = url_re.sub('<URL>',text)
	tokens = split_tokens_re.split(text)
	tokens = [t.lower() if len(t)>1 and len(upper_re.findall(t))<2 else t for t in tokens]
	#tokens = [t.lower() for t in tokens]
	tokens = ['<NUM>' if num_re.match(t) else t for t in tokens]
	return tokens

# ------------------------------------------------------------------------------

from time import time
t0 = time()
from model import HoracyModel
model = HoracyModel('model_100/')
model.text_to_sentences = text_to_sentences
model.text_to_tokens = text_to_tokens
model.doc_to_text = doc_to_text
if 1: # init
	import data
	limit = 100
	model.init_meta(data.doc_iter(limit), get_meta)
	model.init_sentencer(data.doc_iter(limit))
	#model.explain_sentencer(data.doc_iter(limit),100)
	model.init_phraser(data.doc_iter(limit), **phraser_cfg)
	model.init_phrased(data.doc_iter(limit))
	model.init_dictionary(save=False)
	model.prune_dictionary(**prune_cfg)
	model.init_bow()
	#model.phrased.delete() # del
	model.init_tfidf(**tfidf_cfg)
	model.init_sparse()
	#model.bow.delete() # del
	#model.init_lsi(num_topics=50, id2word=model.dictionary)
	#model.init_lsi(**lsi_cfg)
	#model.init_dense() # TODO transformation=self.lsi
	#model.init_dense_ann(post=2)
	#model.dense.delete() # del
	#model.init_sparse_ann(post=2)
	#model.sparse.delete() # del
else:
	model.load_meta()
	model.load_cleaner()
	model.load_phraser()
	model.load_phrased()
	model.load_dictionary()
	model.load_tfidf()
	model.load_lsi()
	#
	model.load_sparse()
	model.load_dense()

if 1:
	model.init_lsi(**lsi_cfg)
	model.init_dense() # TODO transformation=self.lsi
	# --- DENSE ---
	model.init_dense_ann()
	#model.init_dense_ann(post=2)
	#model.init_dense_ann('brute_force',save=False)
	#model.init_dense_ann('brute_force',space='angulardist',save=False)
	
	# --- SPARSE---
	model.init_sparse_ann()
	#model.init_sparse_ann(M=50)
	#model.init_sparse_ann(post=1)
	#model.init_sparse_ann(post=2)
	#model.init_sparse_ann(post=2,M=100)
	#model.init_sparse_ann(method='simple_invindx',space='negdotprod_sparse_fast',save=False)
	#model.init_sparse_ann(method='brute_force',space='cosinesimil_sparse',save=False)
	#model.init_sparse_ann(method='brute_force',space='negdotprod_sparse',save=False)
	#model.init_sparse_ann(method='brute_force',space='angulardist_sparse',save=False)
	#model.init_sparse_ann(method='brute_force',space='l1_sparse',save=False)
	#model.init_sparse_ann(method='brute_force',space='l2_sparse',save=False)
	#model.init_sparse_ann(method='brute_force',space='linf_sparse',save=True)
else:
	model.load_sparse_ann()
	model.load_dense_ann()

print('\ntotal:',time()-t0,'\n\n')


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

i = 5

import sys
import data
query = 'test ventilation outbreak test Wuhan model modeling'
query = 'TWIRLS test'
query = 'ventilation data table'
query = 'homemade'
query = 'sugar'
query = 'Malaysia'
query = 'MERS'
query = 'The Viral Protein Corona Directs Viral Pathogenesis and Amyloid Aggregation'
query = 'RNA'
query = 'ACE2'
query = 'Potential impact of seasonal forcing'
query = 'Zika'
query = 'reinfection'
query = 'TWIRLS'
query = 'VP3, and VP0 (which is further processed to VP2 and VP4'
m = model.meta[i]
query = model.doc_to_text(data.get_doc(m['path'],m['text_id']))
#query = 'sex sexual sexually partner intimate behavior'

print(f'QUERY:\n{query}')
print(f'sparse[{i}]:',len(model.sparse[i]),model.sparse[i])
print(f'dense[{i}]:',len(model.dense[i]),model.dense[i])
#print(f'\nsparse_ann[{i}]:',len(model.sparse_ann[i]),model.sparse_ann[i])
#print(f'\ndense_ann[{i}]:',len(model.dense_ann[i]),model.dense_ann[i])
#print()
#print()

if 1:
	print('\nDENSE:')
	print('\ndense query:',model.text_to_dense(query),'\n')
	top = model.find_dense(query)
	for id,score,m in top:
		doc = data.get_doc(m['path'],m['text_id'])
		print(id,round(score,2),model.explain(id),sep='   ')

if 1:
	print('\nSPARSE:')
	print('\nsparse query:',model.text_to_sparse(query),'\n')
	top = model.find_sparse(query)
	for id,score,m in top:
		doc = data.get_doc(m['path'],m['text_id'])
		print(id,round(score,2),model.explain(id),sep='   ')

#print(list(model.text_to_phrased('the nipah virus september')))

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

from random import randint
ids = [randint(0,len(model.meta)) for _ in range(1000)]
print('sparse score:',test_model(ids, model.find_sparse))
print('dense score: ',test_model(ids, model.find_dense))

