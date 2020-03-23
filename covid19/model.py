from model_text       import HoracyText
from model_input      import HoracyInput
from model_phraser    import HoracyPhraser
from model_dictionary import HoracyDictionary
from model_bow        import HoracyBOW
from model_tfidf      import HoracyTFIDF

from util_time import timed

class HoracyModel(
		HoracyText,
		HoracyInput,
		HoracyPhraser,
		HoracyDictionary,
		HoracyBOW,
		HoracyTFIDF):
	
	@timed
	def find(self, query):
		scored = []
		if type(query) is not dict:
			query = {query:1}
		q_weight = []
		for text,weight in query.items():
			q = self.text_to_sparse(text)
			q_weight += [(q,weight)]
		for doc in self.sparse:
			id = 0 # TODO
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
		self.load_phraser()
		self.load_dictionary()
		self.load_tfidf()
	
	def save(self):
		# TODO path prefix
		self.save_phraser()
		self.save_phrased()
		self.save_dictionary()
		self.save_bow() # ???
		self.save_tfidf()
		self.save_sparse() # ???

# ------------------------------------------------------------------------------

if __name__=="__main__":
	model = HoracyModel()
	# init
	model.init_phraser(100)
	model.init_phrased(100)
	model.init_dictionary()
	model.init_bow()
	model.init_tfidf()
	model.init_sparse()
	# save
	model.save()
	#
	query = 'test ventilation outbreak test Wuhan'
	print(model.text_to_sparse(query))
	print(model.find({query:10}))
