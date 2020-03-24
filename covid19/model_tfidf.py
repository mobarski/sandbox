from gensim.models import TfidfModel
from sorbet import sorbet

from util_time import timed

# ---[ MODEL ]------------------------------------------------------------------

class HoracyTFIDF():
	
	@timed
	def init_tfidf(self, **kwargs):
		self.tfidf = TfidfModel(self.bow, **kwargs)
		self.tfidf.save('model/tfidf.pkl')
	
	@timed
	def load_tfidf(self):
		self.tfidf = TfidfModel.load('model/tfidf.pkl')

	@timed
	def init_sparse(self, materialize=True):
		sparse = (dict(self.tfidf[bow]) for bow in self.bow)
		self.sparse = sorbet('model/sparse').dump(sparse)
		
	@timed
	def load_sparse(self):
		self.sparse = sorbet('model/sparse').load()

# ---[ DEBUG ]------------------------------------------------------------------

if __name__=="__main__":
	model = HoracyTFIDF()
	model.load_tfidf()
	#
	pass
