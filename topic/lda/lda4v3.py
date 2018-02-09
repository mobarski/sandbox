# encoding: utf8

# -> http://brooksandrew.github.io/simpleblog/articles/latent-dirichlet-allocation-under-the-hood/

import re
from random import *
from collections import Counter
from pprint import pprint
from heapq import nlargest
from time import time

K = 2
ITERATIONS = 10
N = 6
alpha = 0.1 # document factor
eta = 0.1 # word factor
RANDOMIZE = False

documents = [
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

def get_tf(text):
	terms = re.findall('(?u)\w+',text.lower())
	#terms = [t for t in terms if t not in set(['sa','na','z'])]
	terms = [t for t in terms if len(t)>=4]
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

#print(weighted_choice({11:.1,22:.1,33:.1}))

docs = list(map(get_tf,documents))
corpus = Counter()
for doc in docs:
	corpus.update(doc)
corpus = dict(corpus)

# TODO min_df

topics = list(range(1,K+1))

# initialize
topic_of_doc_word = {d:{} for d in range(len(docs))}
n_doc_to_topic = {d:{t:0 for t in topics} for d in range(len(docs))} # ~fi
n_word_to_topic = {w:{t:0 for t in topics} for w in corpus} # ~beta
p_doc_to_topic = {d:{t:0.0 for t in topics} for d in range(len(docs))} # phi
p_word_to_topic = {w:{t:0.0 for t in topics} for w in corpus} # beta
total_in_topic = {t:0 for t in topics}
## pass # gamma

# randomly select new topic for word in document
i=0
for d,doc in enumerate(docs):
	for w in doc:
		t = randint(1,K) if RANDOMIZE else (i%K)+1
		topic_of_doc_word[d][w] = t
		total_in_topic[t] += 1
		n_doc_to_topic[d][t] += 1
		n_word_to_topic[w][t] += 1
		i += 1

# calculate probabilities
for w in n_word_to_topic:
	total = sum(n_word_to_topic[w].values()) + eta*len(topics)
	p_word_to_topic[w] = {t:1.*(n_word_to_topic[w][t]+eta)/total for t in topics}
for d in n_doc_to_topic:
	total = sum(n_doc_to_topic[d].values()) + alpha*len(topics)
	p_doc_to_topic[d] = {t:1.*(n_doc_to_topic[d][t]+alpha)/total for t in topics}

if 1:
	pprint(topic_of_doc_word)
	pprint(p_doc_to_topic)
	pprint(p_word_to_topic)
	pprint(total_in_topic)
	#exit()

t0=time()
for _ in range(ITERATIONS):
	# select new topic for word in document
	for d,doc in enumerate(docs):
		for w in doc:
			
			total = 0.0
			p_of_t = {}
			for t in topics:
				#p_of_t[t] = 1.* (n_word_to_topic[w][t]+eta) / total_in_topic[t] * (n_doc_to_topic[d][t]+alpha)
				p = 1.* p_word_to_topic[w][t] * p_doc_to_topic[d][t]
				p_of_t[t] = p
				total += p
			for t in topics:
				p_of_t[t] /= total
			#print(p_of_t)
			#exit()
			
			print(d,w,doc,docs[d],topic_of_doc_word[d])
			t = topic_of_doc_word[d][w]
			print(t)
			total_in_topic[t] -= 1
			n_doc_to_topic[d][t] -= 1
			n_word_to_topic[w][t] -= 1
			old_t = t

			t = weighted_choice(p_of_t)

			topic_of_doc_word[d][w] = t
			total_in_topic[t] += 1
			n_doc_to_topic[d][t] += 1
			n_word_to_topic[w][t] += 1

			# calculate probabilities
			for w in n_word_to_topic:
				total = sum(n_word_to_topic[w].values()) + eta*len(topics)
				p_word_to_topic[w] = {t:1.*(n_word_to_topic[w][t]+eta)/total for t in topics}
			for d in n_doc_to_topic:
				total = sum(n_doc_to_topic[d].values()) + alpha*len(topics)
				p_doc_to_topic[d] = {t:1.*(n_doc_to_topic[d][t]+alpha)/total for t in topics}


if 1:
	pprint(n_doc_to_topic)
	pprint(n_word_to_topic)
	pprint(total_in_topic)

print(time()-t0,'s',ITERATIONS/(time()-t0),'iter/s')

# topic best words
by_t = {t:{} for t in topics}
for w in n_word_to_topic:
	#for t,p in n_word_to_topic[w].items():
	for t in n_word_to_topic[w]:
		p = p_word_to_topic[w][t]
		by_t[t][w] = p
for t in by_t:
	total = sum(by_t[t].values())
	for w in by_t[t]:
		by_t[t][w] /= total 
	pprint((t,nlargest(N,by_t[t].items(),key=lambda x:x[1])))
	#print(t,by_t[t])
