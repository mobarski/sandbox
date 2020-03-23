from data import all_records

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

	@staticmethod
	def all_records(limit=None):
		yield from all_records(limit)

	# TODO uzywane chyba w 1 miejscu
	def all_sentences(self, limit=None):
		for rec in all_records(limit):
			text = self.rec_to_text(rec)
			yield from self.text_to_tokens(text)
