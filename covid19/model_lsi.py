from gensim.models import LsiModel
from sorbet import sorbet

from util_time import timed

# ---[ MODEL ]------------------------------------------------------------------

class HoracyLSI():
	
	@timed
	def init_lsi(self, **kwargs):
		corpus = (s.items() for s in self.sparse)
		self.lsi = LsiModel(corpus, **kwargs)
		self.lsi.save(self.path+'lsi.pkl')
	
	@timed
	def load_lsi(self):
		self.lsi = LsiModel.load(self.path+'lsi.pkl')

	@timed
	def init_dense(self):
		corpus = (s.items() for s in self.sparse)
		dense = (self.lsi[c] for c in corpus)
		self.dense = sorbet(self.path+'dense').dump(dense)
		
	@timed
	def load_dense(self):
		self.dense = sorbet(self.path+'dense').load()

# ---[ DEBUG ]------------------------------------------------------------------

if __name__=="__main__":
	model = HoracyLSI()
	model.path = 'model_100/'
	model.load_lsi()
	model.load_dense()
	#
	print(model.dense[0])
