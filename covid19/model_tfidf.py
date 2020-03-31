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
	data = ((i,cnt,tfidf.idfs[i],d.get(i,'???')) for i,cnt in tfidf.dfs.items())
	data = sorted(data,key=lambda x:x[1],reverse=True)
	for i,cnt,idf,token in islice(data,40):
		print(i,cnt,
			round(idf,1),
			token,
			sep='\t')
