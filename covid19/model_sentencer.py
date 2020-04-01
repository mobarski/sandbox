from hashlib import md5
from tqdm import tqdm
import pickle
from collections import Counter

def my_hash(text):
	"""64bit hash from text"""
	return int(md5(text.lower().encode()).hexdigest()[:16],16)

class HoracySentencer:

	def init_sentencer(self, doc_iter):
		sen = Counter()
		cnt = 0
		doc_iter = tqdm(doc_iter, desc='sentencer_input', total=len(self.meta)) # progress bar
		sentences = self.all_sentences(doc_iter, as_tokens=False)
		for text in sentences:
			h = my_hash(text)
			sen[h] += 1
			cnt += 1
		self.sentencer = sen
		pickle.dump(sen, open(self.path+'sentencer.pkl','wb'))
		
	
	def load_sentencer(self):
		self.sentencer = pickle.load(open(self.path+'sentencer.pkl','rb'))

	def all_sentences(self, doc_iter, as_tokens=True):
		for doc in doc_iter:
			text = self.doc_to_text(doc)
			sentences = self.text_to_sentences(text)
			if as_tokens:
				for s in sentences:
					yield self.text_to_tokens(s)
			else:
				yield from sentences

	def explain_sentencer(self, doc_iter, k):
		top = self.sentencer.most_common(k)
		top_ids = set([x[0] for x in top])
		top_text = {}
		for text in self.all_sentences(doc_iter ,as_tokens=False):
			h = my_hash(text)
			if h in top_ids:
				top_text[h] = text
		for id,cnt in top:
			print(cnt,id,top_text[id])



if __name__ == "__main__":
	import data
	model = HoracySentencer()
	model.path = 'model_100/'
	model.load_sentencer()
	