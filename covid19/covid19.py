
phraser_cfg = {
	'min_count' : 3,
	'threshold' : 1.0,
	'delimiter' : b'__',
	'common_terms' : [
		'','to','and','of','the','a','an','in','by','for','on','that','or',
		'was','this','then','than','is','with','/','*','+','-','=','<','>',
		'could','be','here','we','has','are','there','as','did','not',
		'from','may','have','from','our','et','al','under','were','these',
		'at','out','but','also','it','into','de','one','two','had','no','not','so'
	],
}

def get_meta(id,doc):
	m = {f:doc[f] for f in ['paper_id','text_id','paper_title','path']}
	m['id'] = id # DEBUG
	return m

def doc_to_text(doc):
	values = [
			doc['section'],
			doc['text'],
			'\n'.join(doc['tables']),
			'\n'.join(doc['figures']),
			'\n'.join(doc['bib_titles'])
		]
	return '\n\n'.join(values)

import re
split_sentences_re = re.compile('(?<!.prof|et al)[.?!]+ (?=[A-Z])')
split_tokens_re = re.compile('[\s.,;!?()\[\]]+')
upper_re = re.compile('[A-Z]')

num_re = re.compile('\d+|\d+[%]|\d+[a-z]|[#]\d+|[~]\d+')
url_re = re.compile('[hH][tT][tT][pP][sS]?://[a-zA-Z._0-9/=&?,|%-]+')

def text_to_sentences(text):
	return split_sentences_re.split(text)

def text_to_tokens(text):
	text = url_re.sub('<URL>',text)
	tokens = split_tokens_re.split(text)
	tokens = [t.lower() if len(t)>1 and len(upper_re.findall(t))<2 else t for t in tokens]
	tokens = ['<NUM>' if num_re.match(t) else t for t in tokens]
	return tokens

from time import time
t0 = time()
from model import HoracyModel
model = HoracyModel('model_100/')
model.text_to_sentences = text_to_sentences
model.text_to_tokens = text_to_tokens
model.doc_to_text = doc_to_text
if 0: # init
	import data
	limit = 100
	model.init_meta(data.doc_iter(limit), get_meta)
	model.init_phraser(data.doc_iter(limit), **phraser_cfg)
	model.init_phrased(data.doc_iter(limit))
	model.init_dictionary()
	model.prune_dictionary(no_below=2,no_above=0.5,keep_tokens=['<PAD>','<NUM>'])
	model.init_bow()
	#model.phrased.delete() # del
	model.init_tfidf()
	model.init_sparse()
	#model.bow.delete() # del
	model.init_lsi(num_topics=50, id2word=model.dictionary)
	model.init_dense() # TODO transformation=self.lsi
	model.init_dense_ann()
	#model.dense.delete() # del
	model.init_sparse_ann()
	#model.sparse.delete() # del
else: # load
	model.load_meta()
	model.load_phraser()
	model.load_phrased()
	model.load_dictionary()
	model.load_tfidf()
	model.load_lsi()
	model.load_sparse_ann()
	model.load_dense_ann()

print('\ntotal:',time()-t0,'\n\n')

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
query = 'TWIRLS'
query = 'reinfection'
m = model.meta[3]
query = model.doc_to_text(data.get_doc(m['path'],m['text_id']))
print(f'query: {query}')
print('sparse query:',model.text_to_sparse(query))
i = 1
#print(f'sparse[{i}]:',len(model.sparse[i]),model.sparse[i])
#print(f'dense[{i}]:',len(model.dense[i]),model.dense[i])
print(f'sparse_ann[{i}]:',len(model.sparse_ann[i]),model.sparse_ann[i])
print(f'dense_ann[{i}]:',len(model.dense_ann[i]),model.dense_ann[i])
print()
#print('dense:',model.text_to_dense(query))
print()

print('DENSE:')
top = model.find_dense(query)
for id,score,m in top:
	doc = data.get_doc(m['path'],m['text_id'])
	print(id,round(score,3),model.phrased[id][:10],'###',doc['text'],doc['bib_titles'],doc['tables'],doc['figures'])

print('\nSPARSE:')
top = model.find_sparse(query)
for id,score,m in top:
	doc = data.get_doc(m['path'],m['text_id'])
	print(id,round(score,3),model.phrased[id][:10],'###',doc['text'],doc['bib_titles'],doc['tables'],doc['figures'])
