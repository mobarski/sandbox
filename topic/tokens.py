from contrib import *
import re


def tokenize(text):
	tokens = re.findall('(?u)[\w.-]+',text)
	tokens = [t for t in tokens if not re.match('[\d.-]+$',t)]
	#tokens = [t for t in tokens if len(t)>2]
	# TODO remove stopwords
	return u' '.join(tokens)

## text = KV('data/text.db',5)
## tokens = KV('data/tokens.db',5)
text = PDM().load('data/text.pd')
tokens = PDM().load('data/tokens.pd')
for k,v in text.items():
	print(k)
	tokens[k] = tokenize(v.decode('utf8'))
tokens.save('data/tokens.pd')
