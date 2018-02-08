# encoding: utf8

import re
from random import *
from collections import Counter
from pprint import pprint
from heapq import nlargest
from time import time

# -> http://obphio.us/pdfs/lda_tutorial.pdf
# -> http://brooksandrew.github.io/simpleblog/articles/latent-dirichlet-allocation-under-the-hood/

K = 6
ITERATIONS = 1000
N = 6
alpha = 0.1 # document alpha factor
eta = 0.1 # word eta factor
RANDOMIZE = False

documents = [
"reksio czesto szczeka na koty",
"pies czasem glosno szczeka",
"koty czestp cicho mrucza",
"reksio to madry pies",
"kerbale czesto buduja rakiety",
"rakiety czasem wynosza satelity",
"satelity zawsze sa na orbicie",
"rakiety zawsze glosno startuja",
"szybowce zawsze leca cicho",
"szybowce czasem startuja z wyciagarki",
"samoloty szturmowe czesto leca nisko",
"krowy czesto jedza trawe",
"kury czesto jedza ziarno",
"krowy czesto pija wode",
"ciagnik czasem wiezie ziarno na przyczepie",
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
t_of_w_in_d = {w:{} for w in corpus}
total_d_in_t = {d:{t:0 for t in topics} for d in range(len(docs))} # ~phi
total_w_in_t = {w:{t:0 for t in topics} for w in corpus} # ~theta
total_in_t = {t:0 for t in topics}
## pass # gamma

# randomly select new topic for word in document
i=0
for d,doc in enumerate(docs):
	for w in doc:
		t = randint(1,K) if RANDOMIZE else (i%K)+1
		t_of_w_in_d[w][d] = t
		total_in_t[t] += 1
		total_d_in_t[d][t] += 1
		total_w_in_t[w][t] += 1
		i += 1

if 0:
	pprint(total_d_in_t)
	pprint(total_w_in_t)
	pprint(total_in_t)
	#exit()

t0=time()
for _ in range(ITERATIONS):
	# select new topic for word in document
	for d,doc in enumerate(docs):
		for w in doc:
			
			# gdzie to powinno byc?
			t = t_of_w_in_d[w][d]
			total_in_t[t] -= 1
			total_d_in_t[d][t] -= 1
			total_w_in_t[w][t] -= 1
			old_t = t

			p_of_t = {}
			for t in topics:
				# ??? czu tu nie powinna powstac macierz kwadratowa?
				denom_a = len(doc) + K*alpha
				denom_b = total_in_t[t] + len(corpus)*eta
				p_of_word_in_t = 1.* (total_w_in_t[w][t] + eta)   / denom_b
				p_of_t_in_doc  = 1.* (total_d_in_t[d][t] + alpha) / denom_a
				p_of_t[t] = p_of_word_in_t * p_of_t_in_doc
				#print(d,w,t,p_of_word_in_t,p_of_t_in_doc)
			#print(p_of_t)
			
			t = weighted_choice(p_of_t)

			t_of_w_in_d[w][d] = t
			total_in_t[t] += 1
			total_d_in_t[d][t] += 1
			total_w_in_t[w][t] += 1

if 1:
	pprint(total_d_in_t)
	pprint(total_w_in_t)
	pprint(total_in_t)


# theta - topics probabilities per document
p_d_in_t = {d:{} for d in range(len(docs))}
for d,doc in enumerate(docs):
	denom_a = 1.* len(doc) + K*alpha
	for t in topics:
		p_d_in_t[d][t] = 1.* (total_d_in_t[d][t] + alpha) / denom_a
pprint(p_d_in_t)

# phi - topic probabilities per word
p_w_in_t = {w:{} for w in corpus} # phi
for w in corpus:
	for t in topics:
		denom_b = total_in_t[t] + len(corpus)*eta
		p_w_in_t[w][t] = 1.* (total_w_in_t[w][t] + eta) / denom_b
pprint(p_w_in_t)

print(time()-t0,'s',ITERATIONS/(time()-t0),'iter/s')

# topic best words
by_t = {t:{} for t in topics}
for w in p_w_in_t:
	for t in total_w_in_t[w]:
		p = p_w_in_t[w][t]
		by_t[t][w] = p
for t in by_t:
	total = sum(by_t[t].values())
	for w in by_t[t]:
		by_t[t][w] /= total 
	pprint((t,nlargest(N,by_t[t].items(),key=lambda x:x[1])))
	#print(t,by_t[t])
