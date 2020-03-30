import os
import re
from tqdm import tqdm

from model_meta       import HoracyMeta
from model_phraser    import HoracyPhraser
from model_dictionary import HoracyDictionary
from model_tfidf      import HoracyTFIDF
from model_lsi        import HoracyLSI
from model_ann        import HoracyANN

from util_time import timed

split_sentences_re = re.compile('[.?!]+ (?=[A-Z])')
split_tokens_re = re.compile('[\s.,;!?()\[\]]+')

class HoracyModel(
		HoracyMeta,
		HoracyPhraser,
		HoracyDictionary,
		HoracyTFIDF,
		HoracyLSI,
		HoracyANN
	):
	
	def __init__(self, path='model/'):
		self.path = path
		# create model directory if not exists
		model_dir = os.path.dirname(path)
		if not os.path.exists(model_dir):
			os.makedirs(model_dir)
	
	# porzucamy to podejscie -> zbyt wolne
	@timed
	def find_old(self, query):
		scored = []
		if type(query) is not dict:
			query = {query:1}
		q_weight = []
		for text,weight in query.items():
			q = self.text_to_sparse(text)
			q_weight += [(q,weight)]
		sparse = self.sparse
		sparse = tqdm(sparse, desc='find', total=len(sparse))
		for id,doc in enumerate(sparse):
			for q,weight in q_weight:
				score = sum((doc.get(token,0) for token,_ in q)) * weight
				if score>0:
					scored.append((id,score))
		scored.sort(key=lambda x:x[1],reverse=True)
		return scored
	
	@timed
	def find_sparse(self, text):
		sparse = self.text_to_sparse(text)
		i_list,d_list = self.sparse_ann_query(sparse)
		for i,d in zip(i_list,d_list):
			m = self.meta[i]
			yield i,d,m

	@timed
	def find_dense(self, text):
		dense = self.text_to_dense(text)
		i_list,d_list = self.dense_ann_query(dense)
		for i,d in zip(i_list,d_list):
			m = self.meta[i]
			yield i,d,m

	def text_to_sparse(self, text):
		phrased = self.text_to_phrased(text)
		bow = self.dictionary.doc2bow(phrased)
		return self.tfidf[bow]
	
	def text_to_dense(self, text):
		sparse = self.text_to_sparse(text)
		return self.lsi[sparse]

	@staticmethod
	def text_to_sentences(text):
		return split_sentences_re.split(text)

	@staticmethod
	def text_to_tokens(text):
		tokens = split_tokens_re.split(text)
		return [t.lower() for t in tokens]

	@staticmethod
	def doc_to_text(doc):
		values = [x for x in doc.values() if type(x) is str]
		return '\n\n'.join(values)

	# TODO opcjonalne ladowanie (lsi, dense, ann_sparse, ann_dense)
	def load(self):
		self.load_meta()
		self.load_phraser()
		self.load_dictionary()
		self.load_tfidf()
		#self.load_lsi()
		#self.load_ann()
		#
		#self.load_phrased()
		#self.load_bow()
		#self.load_sparse()
		#self.load_dense()
		#
		return self

# ------------------------------------------------------------------------------

if __name__=="__main__":
	pass
