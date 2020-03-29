from gensim.corpora.dictionary import Dictionary
from tqdm import tqdm

from util_time import timed
from sorbet import sorbet

# ---[ MODEL ]------------------------------------------------------------------

class HoracyDictionary():
	
	#@timed
	def init_dictionary(self):
		phrased = self.phrased
		phrased = tqdm(phrased, desc='dictionary', total=len(phrased))
		self.dictionary = Dictionary(phrased)
		self.dictionary.patch_with_special_tokens({'<PAD>':0})
		self.dictionary.save(self.path+'dictionary.pkl')
	
	#@timed
	def load_dictionary(self):
		self.dictionary = Dictionary.load(self.path+'dictionary.pkl')

	@timed
	def prune_dictionary(self, **kwargs):
		self.dictionary.filter_extremes(**kwargs)

	@timed
	def init_bow(self):
		self.bow = sorbet(self.path+'bow').new()
		phrased = tqdm(self.phrased, desc='bow', total=len(self.phrased)) # progress bar
		for doc in phrased:
			bow = self.dictionary.doc2bow(doc) or [(0,1)]
			self.bow.append(bow)
		self.bow.save()
	
	#@timed
	def load_bow(self):
		self.bow = sorbet(self.path+'bow').load()

# ---[ DEBUG ]------------------------------------------------------------------

if __name__=="__main__":
	model = HoracyDictionary()
	model.path = 'model_100/'
	model.load_dictionary()
	#
	d = list(model.dictionary.dfs.items())
	d.sort(key=lambda x:-x[1])
	for id,cnt in d[:60]:
		token = model.dictionary.get(id)
		print(f"{cnt:4d} {token}")
	print('phrases:')
	i=0
	for id,cnt in d:
		token = model.dictionary.get(id)
		if '__' not in token: continue
		print(f"{cnt:4d} {token}")
		i+=1
		if i>200:break

