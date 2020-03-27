import re

from model import HoracyModel
import data

phraser_cfg = {
	'min_count' : 3,
	'threshold' : 1.0,
	'delimiter' : b'__',
	'common_terms' : [
		'','to','and','of','the','a','an','in','by','for','on','that','or',
		'was','this','then','than','is','with','/','*','+','-','=',
		'could','be','here','we','has','are','there','as','did','not',
		'from','may','have','from','our','et','al','under','were','these',
		'at','out','but','also','it','into','de','one','two','had','no','not','so'
	],
}

def get_meta(id,doc):
	m = {f:doc[f] for f in ['paper_id','text_id','paper_title']}
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

split_sentences_re = re.compile('(?<!.prof|et al)[.?!]+ (?=[A-Z])')
split_tokens_re = re.compile('[\s.,;!?()\[\]]+')
upper_re = re.compile('[A-Z]')

def text_to_sentences(text):
	return split_sentences_re.split(text)

def text_to_tokens(text):
	tokens = split_tokens_re.split(text)
	return [t.lower() if len(t)>1 and len(upper_re.findall(t))<2 else t for t in tokens]

# calculation time:
#   8000 -> 3094s
#   4000 -> 1351s
#   2000 -> 512s
#   1000 -> 202s
#    100 -> 21s
model = HoracyModel('model_100/')
model.text_to_sentences = text_to_sentences
model.text_to_tokens = text_to_tokens
model.doc_to_text = doc_to_text
if 1: # init
	limit = 100
	model.init_meta(data.doc_iter(limit), get_meta)
	model.init_phraser(data.doc_iter(limit), **phraser_cfg)
	model.init_phrased(data.doc_iter(limit))
	model.init_dictionary()
	model.init_bow()
	model.init_tfidf()
	model.init_sparse()
	model.init_lsi(num_topics=50, id2word=model.dictionary)
	model.init_dense() # TODO transformation=self.lsi
else: # load
	model.load()


from time import time
import sys
t0 = time()
query = 'test ventilation outbreak test Wuhan model modeling'
query = 'TWIRLS test'
query = 'ACE2'
query = 'TWIRLS'
query = 'ventilation data table'
query = 'sugar'
query = 'homemade'
print()
print('sparse:',model.text_to_sparse(query))
print('dense:',model.text_to_dense(query))
print()
#top = model.find({query:10})[:10]
sys.stderr.flush()
sys.stdout.flush()
top = model.find(query)[:10]
print()
for id,score in top:
	m = model.meta[id]
	print(id,round(score,3),m['paper_title'],'###',' '.join(model.phrased[id]))
print('\n',time()-t0)

