import re

split_sentences_re = re.compile('(?<!.prof|et al)[.?!]+ (?=[A-Z])')
def text_to_sentences(text):
	return split_sentences_re.split(text)

split_tokens_re = re.compile('[\s.,;!?()\[\]]+')
upper_re = re.compile('[A-Z]')
def text_to_tokens(text):
	tokens = split_tokens_re.split(text)
	return [t.lower() if len(upper_re.findall(t))<2 else t for t in tokens]

if __name__=="__main__":
	print(text_to_sentences('Co? To nie tak! OK. Jak chcesz. Wang et al. Smith ok. Hello prof. Richard Johnson. How are you?'))
