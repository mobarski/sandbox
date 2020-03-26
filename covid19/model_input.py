from tqdm import tqdm
from sorbet import sorbet

from data import all_records
from util_time import timed

class HoracyInput():

	@staticmethod
	def rec_to_text(rec):
		values = [
				rec['section'],
				rec['text'],
				'\n'.join(rec['tables']),
				'\n'.join(rec['figures']),
				'\n'.join(rec['bib_titles'])
			]
		return '\n\n'.join(values)

	#@timed
	def init_meta(self, limit=None):
		self.meta = sorbet(self.path+'meta').new()
		records = all_records(limit)
		records = tqdm(records, desc='meta')
		for id,rec in enumerate(records):
			m = {f:rec[f] for f in ['paper_id','text_id','paper_title']}
			m['id'] = id # DEBUG
			self.meta.append(m)
		self.meta.save()
	
	#@timed
	def load_meta(self):
		self.meta = sorbet(self.path+'meta').load()

	@staticmethod
	def all_records(limit=None):
		yield from all_records(limit)

	# TODO uzywane chyba w 1 miejscu
	def all_sentences(self, limit=None):
		for rec in all_records(limit):
			text = self.rec_to_text(rec)
			yield self.text_to_tokens(text)
