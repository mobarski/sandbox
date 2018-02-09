# encoding: utf8

import re
from random import *
from collections import Counter
from pprint import pprint
from heapq import nlargest
from time import time

# http://blog.echen.me/2011/08/22/introduction-to-latent-dirichlet-allocation/
# https://tedunderwood.com/2012/04/07/topic-modeling-made-just-simple-enough/
# http://obphio.us/pdfs/lda_tutorial.pdf
# -> https://www.kdnuggets.com/2016/07/text-mining-101-topic-modeling.html

K = 3
ITERATIONS = 1000
N = 6
a1 = 0.2 # document alpha factor
a2 = 0.01 # word eta factor
SIMPLE = False

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

## documents = [
## # space
## "Watching a bubble float effortlessly through the @Space_Station may be mesmerizing and beautiful, but that same bubble is also teaching @ISS_Research about how fluids behave differently in microgravity",
## "LIVE: On 7 February 2008, the European Columbus laboratory set sail for humanity’s new world of space - join us live as we celebrate 10 years of achievements and look ahead to the future of human exploration ",
## "Flexing our robotic muscles💪. A new robotic arm – that could be used to assemble spacecraft & future outposts for humans in space – was successfully tested to demonstrate that it is fully operational",
## "Perfect timing -- down to the nanosecond -- is vital to navigation in deep space. More accurate timing = More control. For 20 years, we’ve been “perfecting time” for future deep space exploration. The result? The Deep Space Atomic Clock",
## "Europe prepares to celebrate 10 years of its Columbus lab module at the space station as the crew studies the impacts of living in space",
## # drones
## "Ever fly in a cave? Check out these pilots putting in laps underground!",
## "I think this pilot needs more batteries...How many do you bring to the field?",
## "This drone is built for tricks! What do you think about seeing Freestyle in MultiGP?",
## "Hey everyone hope you have an awesome time at the 2018 Sebring Drone Race presented by Soaring Sky. Here's what we have planned for today! ",
## "An army of Racing Drones, getting ready to FLY!!!",
## "Jordan Temkin (@jet.fpv) showing his drone racing skills here in Sebring 2018 day 1!!! ",
## # games
## "We've opened up a public Upcoming Beta branch on Steam so our most eager of Trailmakers can check out upcoming patches! Check out the notes and a tease of more news soon here! ",
## "Hey guys! We’re hearing reports that Humble have revoked some of the pre-order keys, we’re not sure why but if you log into your Humble account, go to Purchases and activate the key from there again you’ll get Trailmakers back on your Steam account! Sorry about this!",
## "We've deployed a small update with some critical fixes to Trailmakers! Read the notes",
## "Build any vehicle you can dream up, and race it around an alien planet. This is for you grease monkeys. Trailmakers is coming out on Wednesday! ",
## "Did you pre-order Trailmakers? We just sent you an e-mail asking what name/nickname you want us to put on - THE MONUMENT!",
## "We're seeing a lot of feedback coming in from people playing the 10 month old Alpha demo. We love your feedback, but we'd love it even more if you were trying the new Alpha 2. Trailmakers should look like this in your Steam List if you're on the right build!"
## ]


def get_tf(text):
	terms = re.findall('(?u)\w+',text.lower())
	terms = [t for t in terms if t not in set(['sa','na','z'])]
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
p_of_d_in_t = {d:{t:1./K for t in topics} for d in range(len(docs))} # fi
p_of_w_in_t = {w:{t:0 for t in topics} for w in corpus} # beta
t_of_w = {w:{} for w in corpus}
## pass # gamma

# randomly select new topic for word
for w in t_of_w:
	t_of_w[w] = randint(1,K)

t0=time()
for _ in range(ITERATIONS):
	# recalculate document in topic probability
	for d,doc in enumerate(docs):
		by_t = {t:0 for t in topics}
		for w in doc:
			t = t_of_w[w]
			by_t[t] += 1
		total = sum(by_t.values())
		p_of_d_in_t[d] = {t:1.*(by_t[t]+a1)/total for t in topics}
	# recalculate word in topic probability
	for w in corpus:
		by_t = {t:0 for t in topics}
		for d,doc in enumerate(docs):
			if w not in doc: continue
			for t in topics:
				by_t[t] += p_of_d_in_t[d][t]
		total = sum(by_t.values())
		p_of_w_in_t[w] = {t:1.*(by_t[t]+a2)/total for t in topics}

	# select new topic for word in document
	for d,doc in enumerate(docs):
		for w in doc:
			if SIMPLE: # nie wiem ktora wersja jest poprawna !!!
				t = weighted_choice(p_of_d_in_t[d])
			else:
				p_of_t = p_of_d_in_t[d]
				for t in topics:
					p_of_t[t] = p_of_t[t] * p_of_w_in_t[w][t]
				t = weighted_choice(p_of_t)
			t_of_w[w] = t


#pprint(p_of_d_in_t)
#pprint(p_of_w_in_t)

print(time()-t0,'s',ITERATIONS/(time()-t0),'iter/s')

# topic best words
by_t = {t:{} for t in topics}
for w in p_of_w_in_t:
	#for t,p in p_of_w_in_t[w].items():
	for t in p_of_w_in_t[w]:
		p = p_of_w_in_t[w][t]
		by_t[t][w] = p
for t in by_t:
	total = sum(by_t[t].values())
	for w in by_t[t]:
		by_t[t][w] /= total
		#pass
	pprint((t,nlargest(N,by_t[t].items(),key=lambda x:x[1])))
	#print(t,by_t[t])
