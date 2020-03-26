from gensim.models.phrases import Phrases, Phraser
from tqdm import tqdm
from sorbet import sorbet

# from data import all_sentences_as_tokens
# from data import all_records_as_tokens
from util_time import timed

# ---[ MODEL ]------------------------------------------------------------------

MIN_COUNT = 3
THRESHOLD = 1.0
DELIMITER = b'__'
COMMON_TERMS = [
	'','to','and','of','the','a','an','in','by','for','on','that','or',
	'was','this','then','than','is','with','/','*','+','-','=',
	'could','be','here','we','has','are','there','as','did','not',
	'from','may','have','from','our','et','al','under','were','these',
	'at','out','but','also','it','into','de','one','two','had','no','not','so'
]

class HoracyPhraser():

	@timed
	def init_phraser(self, limit=None):
		sentences = self.all_sentences(limit)
		sentences = tqdm(sentences, desc='phraser_input', total=len(self.meta)) # progress bar
		phrases = Phrases(sentences,
		                  min_count=MIN_COUNT,
						  threshold=THRESHOLD,
						  delimiter=DELIMITER,
		                  common_terms=COMMON_TERMS)
		self.phraser = Phraser(phrases)
		self.phraser.save(self.path+'phraser.pkl')
		del phrases

	#@timed
	def load_phraser(self):
		self.phraser = Phraser.load(self.path+'phraser.pkl')
	
	# TODO rename rec -> doc
	def rec_to_phrased(self, rec):
		text = self.rec_to_text(rec)
		yield from self.text_to_phrased(text)
	
	def text_to_phrased(self, text):
		sentences = self.text_to_sentences(text)
		for sentence in sentences:
			tokens = self.text_to_tokens(sentence)
			yield from self.phraser[tokens]
	
	#@timed
	def init_phrased(self, limit=None):
		# TODO trzeba zapisac gdzies liste id rekordow -> realizujemy model kolumnowy
		records = self.all_records(limit)
		phrased = (list(self.rec_to_phrased(r)) for r in records)
		phrased = tqdm(phrased, desc='phrased', total=len(self.meta)) # progress bar
		self.phrased = sorbet(self.path+'phrased').dump(phrased)
		
	#@timed
	def load_phrased(self):
		#self.phrased = pickle.load(open('model/phrased.pkl','rb'))
		self.phrased = sorbet(self.path+'phrased').load()

# ---[ DEBUG ]-------------------------------------------------------------------

def count_digits(tokens):
	x = 0
	for token in tokens:
		for letter in token:
			if letter in "0123456789":
				x += 1
	return x

if __name__=="__main__":
	model = HoracyPhraser()
	model.path = 'model_4000/'
	model.load_phraser()
	model.load_phrased()
	#
	from pprint import pprint
	#pprint(model.phrased[0])
	#
	#
	from time import time
	t0=time()
	total = 0
	aaa = {}
	aaa['total'] = 0
	if 0: # 4000 -> 35s
		for tokens in model.phrased:
			x = 0
			for token in tokens:
				for letter in token:
					if letter in "0123456789":
						x += 1
			total += x
	if 1: # 4000 -> 2p:22s
		import multiprocessing as mp
		from tqdm import tqdm
		pool = mp.Pool(processes=2)
		def agg(x):
			aaa['total'] += 1
		#results = pool.map(count_digits, tqdm(model.phrased), 100)
		#results = pool.imap_unordered(count_digits, tqdm(model.phrased), 100)
		results = pool.map_async(count_digits, tqdm(model.phrased), 100, agg)
		for x in results.get():
			total += x
	print(total)
	print(aaa['total'])
	print(f"done in {time()-t0:.02f} seconds")
