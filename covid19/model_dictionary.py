from gensim.corpora.dictionary import Dictionary

from data import all_records_as_tokens
from util_time import timed

class HoracyDictionary():
	
	@timed
	def init_dictionary(self, limit=None):
		records = all_records_as_tokens(limit)
		phrased = self.phraser[records]
		self.dictionary = Dictionary(phrased)
	
	@timed
	def save_dictionary(self):
		self.dictionary.save('model/dictionary.pkl')
	
	@timed
	def load_dictionary(self):
		self.dictionary = Dictionary.load('model/dictionary.pkl')

if __name__=="__main__":
	model = HoracyDictionary()
	model.load_dictionary()
	# inspect
	d = list(model.dictionary.dfs.items())
	d.sort(key=lambda x:-x[1])
	for id,cnt in d[:60]:
		token = model.dictionary.get(id)
		print(f"{cnt:4d} {token}")

