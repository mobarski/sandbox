from gensim.models.phrases import Phrases, Phraser
import pickle

from data import all_sentences_as_tokens
from data import all_records_as_tokens
from util_time import timed

# ---[ MODEL ]------------------------------------------------------------------

MIN_COUNT = 3
THRESHOLD = 1.0
COMMON_TERMS = [
	'to','and','of','the','a','an','in','by','for','on','that','or',
	'was','this','then','than','is','with','/','*','+','-'
]

class HoracyPhraser():

	@timed
	def init_phraser(self, limit=None):
		sentences = all_sentences_as_tokens(limit)
		phrases = Phrases(sentences,
		                  min_count=MIN_COUNT,
						  threshold=THRESHOLD,
		                  common_terms=COMMON_TERMS)
		self.phraser = Phraser(phrases)
		del phrases
	
	@timed
	def save_phraser(self):
		self.phraser.save('model/phraser.pkl')

	@timed
	def load_phraser(self):
		self.phraser = Phraser.load('model/phraser.pkl')
	
	@timed
	def init_phrased(self, limit=None, materialize=True):
		# TODO trzeba zapisac gdzies liste id rekordow -> realizujemy model kolumnowy
		records = all_records_as_tokens(limit)
		phrased = self.phraser[records]
		self.phrased = list(phrased) if materialize else phrased
	
	@timed
	def save_phrased(self):
		pickle.dump(self.phrased, open('model/phrased.pkl','wb'))
	
	@timed
	def load_phrased(self):
		self.phrased = pickle.load(open('model/phrased.pkl','rb'))

# ---[ DEBUG ]-------------------------------------------------------------------

if __name__=="__main__":
	model = HoracyPhraser()
	model.load_phraser()
	model.load_phrased()
	#
	pass
