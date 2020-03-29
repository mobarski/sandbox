from gensim.models import TfidfModel
from tqdm import tqdm
from sorbet import sorbet

from util_time import timed

# ---[ MODEL ]------------------------------------------------------------------

class HoracyTFIDF():
	
	#@timed
	def init_tfidf(self, **kwargs):
		bow = self.bow
		bow = tqdm(bow, desc='tfidf', total=len(bow))
		self.tfidf = TfidfModel(bow, **kwargs)
		self.tfidf.save(self.path+'tfidf.pkl')
	
	#@timed
	def load_tfidf(self):
		self.tfidf = TfidfModel.load(self.path+'tfidf.pkl')

	#@timed
	def init_sparse(self, materialize=True):
		sparse = (self.tfidf[bow] for bow in self.bow)
		sparse = tqdm(sparse, desc='sparse', total=len(self.bow)) # progress bar
		self.sparse = sorbet(self.path+'sparse').dump(sparse)
		
	#@timed
	def load_sparse(self):
		self.sparse = sorbet(self.path+'sparse').load()

# ---[ DEBUG ]------------------------------------------------------------------

if __name__=="__main__":
	model = HoracyTFIDF()
	model.path = 'model_1000x/'
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
	for i,cnt in islice(tfidf.dfs.items(),2000):
		token = d.get(i,'???')
		if '__' not in token: continue
		print(i,token,cnt,
			round(tfidf.idfs[i],2),
			round(tfidf.idfs[i]*cnt,1),
			sep='\t')
