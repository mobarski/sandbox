from gensim.models.phrases import Phrases, Phraser

from data import all_sentences_as_tokens
from util_time import timed

COMMON_TERMS = [
	'to','and','of','the','a','an','in','by','for','on','that','or',
	'was','this','then','than','is','with','/','*','+','-'
]

class HoracyPhraser():

	@timed
	def init_phraser(self, limit=None):
		sentences = all_sentences_as_tokens(limit)
		# TODO configuration (min_count, threshold)
		phrases = Phrases(sentences, min_count=3, threshold=1, common_terms=COMMON_TERMS)
		self.phraser = Phraser(phrases)
		del phrases
	
	@timed
	def save_phraser(self):
		self.phraser.save('model/phraser.pkl')

	@timed
	def load_phraser(self):
		self.phraser = Phraser.load('model/phraser.pkl')

if __name__=="__main__":
	model = HoracyPhraser()
	model.load_phraser()
