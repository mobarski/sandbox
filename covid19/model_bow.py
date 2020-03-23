import pickle

from util_time import timed

# ---[ MODEL ]------------------------------------------------------------------

class HoracyBOW():
	
	@timed
	def init_bow(self, materialize=True):
		bow = (self.dictionary.doc2bow(doc) for doc in self.phrased)
		self.bow = list(bow) if materialize else bow
	
	@timed
	def save_bow(self):
		pickle.dump(self.bow, open('model/bow.pkl','wb'))
	
	@timed
	def load_bow(self):
		self.bow = pickle.load(open('model/bow.pkl','rb'))

# ---[ DEBUG ]------------------------------------------------------------------

if __name__=="__main__":
	model = HoracyBOW()
	model.load_bow()
	#
	pass
