from sorbet import sorbet

from util_time import timed

# ---[ MODEL ]------------------------------------------------------------------

class HoracyBOW():
	
	@timed
	def init_bow(self):
		bow = (self.dictionary.doc2bow(doc) for doc in self.phrased)
		self.bow = sorbet(self.path+'bow').dump(bow)
	
	@timed
	def load_bow(self):
		self.bow = sorbet(self.path+'bow').load()

# ---[ DEBUG ]------------------------------------------------------------------

if __name__=="__main__":
	model = HoracyBOW()
	model.path = 'model_100/'
	model.load_bow()
	#
	pass
