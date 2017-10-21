from contrib import *
import re


def tokenize(text):
	tokens = re.findall('(?u)[\w.-]+',text)
	tokens = [t for t in tokens if not re.match('[\d.-]+$',t)]
	tokens = [t for t in tokens if len(t)>2]
	return u' '.join(tokens)

text = KV('data/text.db',5)
tokens = KV('data/tokens.db',5)
for k,v in text.items():
	print(k)
	tokens[k] = tokenize(v.decode('utf8'))
tokens.sync()
