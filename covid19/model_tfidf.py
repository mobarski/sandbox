from gensim.models import TfidfModel
from sorbet import sorbet

from util_time import timed

# ---[ MODEL ]------------------------------------------------------------------

class HoracyTFIDF():
	
	@timed
	def init_tfidf(self, **kwargs):
		self.tfidf = TfidfModel(self.bow, **kwargs)
		self.tfidf.save(self.path+'tfidf.pkl')
	
	@timed
	def load_tfidf(self):
		self.tfidf = TfidfModel.load(self.path+'tfidf.pkl')

	@timed
	def init_sparse(self, materialize=True):
		sparse = (dict(self.tfidf[bow]) for bow in self.bow)
		self.sparse = sorbet(self.path+'sparse').dump(sparse)
		
	@timed
	def load_sparse(self):
		self.sparse = sorbet(self.path+'sparse').load()

# ---[ DEBUG ]------------------------------------------------------------------

if __name__=="__main__":
	model = HoracyTFIDF()
	model.path = 'model_100/'
	model.load_tfidf()
	tfidf = model.tfidf
	#
	from pprint import pprint
	from itertools import islice
	#
	from model_dictionary import HoracyDictionary
	model2 = HoracyDictionary()
	model2.path = model.path
	model2.load_dictionary()
	d = model2.dictionary
	for i,cnt in islice(tfidf.dfs.items(),1000):
		token = d.get(i,'???')
		if '__' not in token: continue
		print(i,token,cnt,
			round(tfidf.idfs[i],2),
			round(tfidf.idfs[i]*cnt,1),
			sep='\t')
