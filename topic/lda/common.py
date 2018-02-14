# encoding: utf8

import re
from random import random
from collections import Counter
from heapq import nlargest

from analyze import sentences_iter

DOCUMENTS = [
"reksio szczeka na koty",
"pies glosno szczeka",
"koty cicho mrucza",
"reksio to madry pies",
"kerbale buduja rakiety",
"rakiety wynosza satelity",
"satelity sa na orbicie",
"rakiety glosno startuja",
"szybowce leca cicho",
"szybowce startuja z wyciagarki",
"samoloty szturmowe leca nisko",
"krowy jedza trawe",
"kury jedza ziarno",
"krowy pija wode"
]

STOPWORDS = set(re.findall('\w+',"""
	oraz gdzie jako jest tego jego przez jednak przy nich jeszcze nawet kiedy
	tylko siebie temu mnie natomiast tych sobie przed podczas bardzo
	już który też może które która jeżeli jeśli żeby także niż których którym której którego został 
"""))

def get_documents(multi=1):
	#documents = DOCUMENTS
	documents = sentences_iter('onet_text.mrl',20)
	docs = list(map(get_tf,documents))
	return docs*multi

def get_words(docs):
	words = set()
	for doc in docs:
		words.update(doc)
	return words

def get_tf(text):
	terms = re.findall('(?u)\w+',text.lower())
	#terms = [t for t in terms if t not in set(['sa','na','z'])]
	terms = [t for t in terms if len(t)>=4 and t not in STOPWORDS]
	#terms = [t for t in terms if len(t)>=4]
	tf = Counter(terms)
	return dict(tf)

def weighted_choice(w_map):
	items = w_map.items()
	cum_weights = [0]*len(items)
	cum_weights[0] = items[0][1]
	for i,item in enumerate(items):
		if i==0: continue
		w = item[1]
		cum_weights[i] = cum_weights[i-1]+w
	total = cum_weights[-1]
	r = random() * total
	for i,c in enumerate(cum_weights):
		if r<c: return items[i][0]


if __name__=="__main__":
	tf = Counter()
	for doc in get_documents():
		tf.update(doc)
	for x in nlargest(20,tf.items(),key=lambda x:x[1]):
		print(x)


	