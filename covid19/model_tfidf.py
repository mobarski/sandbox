from gensim.models import TfidfModel
import pickle

from util_time import timed

# ---[ MODEL ]------------------------------------------------------------------

class HoracyTFIDF():
	
	@timed
	def init_tfidf(self, **kwargs):
		self.tfidf = TfidfModel(self.bow, **kwargs)
	
	@timed
	def save_tfidf(self):
		self.tfidf.save('model/tfidf.pkl')
	
	@timed
	def load_tfidf(self):
		self.tfidf = TfidfModel.load('model/tfidf.pkl')

	@timed
	def init_sparse(self, materialize=True):
		sparse = (dict(self.tfidf[bow]) for bow in self.bow)
		self.sparse = list(sparse) if materialize else sparse
	
	@timed
	def save_sparse(self):
		pickle.dump(self.sparse, open('model/sparse.pkl','wb'))
	
	@timed
	def load_sparse(self):
		self.sparse = pickle.load(open('model/sparse.pkl','rb'))

# ---[ DEBUG ]------------------------------------------------------------------

if __name__=="__main__":
	model = HoracyTFIDF()
	model.load_tfidf()
	#
	pass
