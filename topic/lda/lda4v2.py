# encoding: utf8

import re
from random import *
from collections import Counter
from pprint import pprint
from heapq import nlargest
from time import time

# http://blog.echen.me/2011/08/22/introduction-to-latent-dirichlet-allocation/
# https://tedunderwood.com/2012/04/07/topic-modeling-made-just-simple-enough/
# -> http://obphio.us/pdfs/lda_tutorial.pdf

K = 4
ITERATIONS = 1000
N = 6
a1 = 0.1 # document alpha factor
a2 = 0.1 # word eta factor
RANDOMIZE = False

documents = [
"reksio szczeka na koty",
"pies glosno szczeka",
#"koty cicho mrucza",
"kerbale buduja rakiety",
"rakiety wynosza satelity",
"satelity sa na orbicie",
#"rakiety glosno startuja",
"szybowce leca cicho",
"szybowce startuja z wyciagarki",
"krowy jedza trawe",
"kury jedza ziarno",
"ciagnik wiezie ziarno na przyczepie",
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
total_d_in_t = {d:{t:0 for t in topics} for d in range(len(docs))} # ~fi
total_w_in_t = {w:{t:0 for t in topics} for w in corpus} # ~beta
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

t0=time()
for _ in range(ITERATIONS):
	# select new topic for word in document
	for d,doc in enumerate(docs):
		for w in doc:
			
			p_of_t = {}
			for t in topics:
				p_of_t[t] = 1.* (total_w_in_t[w][t]+a2) / total_in_t[t] * (total_d_in_t[d][t]+a1)
			#print(p_of_t)
			
			t = t_of_w_in_d[w][d]
			total_in_t[t] -= 1
			total_d_in_t[d][t] -= 1
			total_w_in_t[w][t] -= 1
			old_t = t

			t = weighted_choice(p_of_t)

			t_of_w_in_d[w][d] = t
			total_in_t[t] += 1
			total_d_in_t[d][t] += 1
			total_w_in_t[w][t] += 1

if 1:
	pprint(total_d_in_t)
	pprint(total_w_in_t)
	pprint(total_in_t)

print(time()-t0,'s',ITERATIONS/(time()-t0),'iter/s')

# topic best words
by_t = {t:{} for t in topics}
for w in total_w_in_t:
	#for t,p in total_w_in_t[w].items():
	for t in total_w_in_t[w]:
		p = total_w_in_t[w][t]
		by_t[t][w] = p
for t in by_t:
	total = sum(by_t[t].values())
	## for w in by_t[t]:
		## by_t[t][w] /= total 
	pprint((t,nlargest(N,by_t[t].items(),key=lambda x:x[1])))
	#print(t,by_t[t])
