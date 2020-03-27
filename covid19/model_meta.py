from tqdm import tqdm
from sorbet import sorbet

from util_time import timed

class HoracyMeta():

	#@timed
	def init_meta(self, doc_iter, get_meta):
		self.meta = sorbet(self.path+'meta').new()
		records = doc_iter
		records = tqdm(records, desc='meta')
		for id,rec in enumerate(records):
			m = get_meta(id,rec)
			self.meta.append(m)
		self.meta.save()
	
	#@timed
	def load_meta(self):
		self.meta = sorbet(self.path+'meta').load()
	
	# --- PRZENIESC ------------------------------------------------------------

	# TODO uzywane tylko przez phraser -> przesunac ???
	def all_sentences(self, doc_iter):
		for doc in doc_iter:
			text = self.doc_to_text(doc)
			yield self.text_to_tokens(text)

	