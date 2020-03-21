from gensim.models.phrases import Phrases, Phraser
from time import time

VERBOSE = True

def init(LIMIT):
	from data import all_sentences_as_tokens
	sentences = all_sentences_as_tokens(LIMIT)

	t0=time()
	COMMON_TERMS = ['to','and','of','the','a','an','in','by','for','on','that','or','was','this','then','than','is','with','/','*','+','-']
	phrases = Phrases(sentences, min_count=3, threshold=1, common_terms=COMMON_TERMS)
	phraser = Phraser(phrases)
	phraser.save('model/phraser.pkl')
	print(phrases.vocab) # XXX
	if VERBOSE:
		t1 = time()
		print(f"init done in {t1-t0:.02f} seconds, {LIMIT/(t1-t0):.01f} docs/s")
	del phrases
	return phraser

def load():
	t0=time()
	phraser = Phraser.load('model/phraser.pkl')
	if VERBOSE:
		print(f'load done in {time()-t0:.02f} seconds')
	return phraser

if __name__=="__main__":
	#init(1000)
	phraser = load()
