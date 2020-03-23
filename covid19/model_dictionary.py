from gensim.corpora.dictionary import Dictionary

from util_time import timed

# ---[ MODEL ]------------------------------------------------------------------

class HoracyDictionary():
	
	@timed
	def init_dictionary(self):
		self.dictionary = Dictionary(self.phrased)
	
	@timed
	def save_dictionary(self):
		self.dictionary.save('model/dictionary.pkl')
	
	@timed
	def load_dictionary(self):
		self.dictionary = Dictionary.load('model/dictionary.pkl')

	# TODO bow przeniesc tutaj tak jak phrased w phraser ??? -> raczej tak
	# TODO rename bow -> corpus

# ---[ DEBUG ]------------------------------------------------------------------

if __name__=="__main__":
	model = HoracyDictionary()
	model.load_dictionary()
	#
	d = list(model.dictionary.dfs.items())
	d.sort(key=lambda x:-x[1])
	for id,cnt in d[:60]:
		token = model.dictionary.get(id)
		print(f"{cnt:4d} {token}")

