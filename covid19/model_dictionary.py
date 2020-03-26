from gensim.corpora.dictionary import Dictionary
from tqdm import tqdm

from util_time import timed

# ---[ MODEL ]------------------------------------------------------------------

class HoracyDictionary():
	
	#@timed
	def init_dictionary(self):
		phrased = self.phrased
		phrased = tqdm(phrased, desc='dictionary', total=len(phrased))
		self.dictionary = Dictionary(phrased)
		self.dictionary.save(self.path+'dictionary.pkl')
	
	#@timed
	def load_dictionary(self):
		self.dictionary = Dictionary.load(self.path+'dictionary.pkl')

	# TODO bow przeniesc tutaj tak jak phrased w phraser ??? -> raczej tak
	# TODO rename bow -> corpus

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

