from model_text       import HoracyText
from model_input      import HoracyInput
from model_phraser    import HoracyPhraser
from model_dictionary import HoracyDictionary
from model_bow        import HoracyBOW
from model_tfidf      import HoracyTFIDF
from model_lsi        import HoracyLSI

from util_time import timed

class HoracyModel(
		HoracyText,
		HoracyInput,
		HoracyPhraser,
		HoracyDictionary,
		HoracyBOW,
		HoracyTFIDF,
		HoracyLSI
	):
	
	# porzucamy to podejscie -> zbyt wolne
	@timed
	def find(self, query):
		scored = []
		if type(query) is not dict:
			query = {query:1}
		q_weight = []
		for text,weight in query.items():
			q = self.text_to_sparse(text)
			q_weight += [(q,weight)]
		for id,doc in enumerate(self.sparse):
			for q,weight in q_weight:
				score = sum((doc.get(token,0) for token,_ in q)) * weight
				if score>0:
					scored.append((id,score))
		scored.sort(key=lambda x:x[1],reverse=True)
		return scored

	def text_to_sparse(self, text):
		phrased = self.text_to_phrased(text)
		bow = self.dictionary.doc2bow(phrased)
		return self.tfidf[bow]

	def load(self):
		# TODO path prefix
		self.load_meta()
		self.load_phraser()
		self.load_dictionary()
		self.load_tfidf()
		self.load_lsi()
		#
		self.load_phrased()
		self.load_bow()
		self.load_sparse()
		self.load_dense()

# ------------------------------------------------------------------------------

if __name__=="__main__":
	model = HoracyModel()
	if 0:
		# init
		model.init_meta(1000)
		model.init_phraser(1000)
		model.init_phrased(1000)
		model.init_dictionary()
		model.init_bow()
		model.init_tfidf()
		model.init_sparse()
		model.init_lsi(num_topics=50, id2word=model.dictionary)
		model.init_dense()
	else:
		model.load()
	#
	query = 'test ventilation outbreak test Wuhan model modeling'
	query = 'TWIRLS test'
	query = 'ACE2'
	query = 'TWIRLS'
	query = 'ventilation data table'
	query = 'sugar'
	query = 'homemade'
	print(model.text_to_sparse(query))
	#top = model.find({query:10})[:10]
	top = model.find(query)[:10]
	for id,score in top:
		m = model.meta[id]
		print(id,round(score,3),m['paper_title'],'###',' '.join(model.phrased[id]))
