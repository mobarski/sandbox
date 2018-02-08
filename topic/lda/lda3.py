import re
from random import *
from collections import Counter
from pprint import pprint

# http://blog.echen.me/2011/08/22/introduction-to-latent-dirichlet-allocation/
# https://tedunderwood.com/2012/04/07/topic-modeling-made-just-simple-enough/

documents = [
# space
"Watching a bubble float effortlessly through the @Space_Station may be mesmerizing and beautiful, but that same bubble is also teaching @ISS_Research about how fluids behave differently in microgravity",
"LIVE: On 7 February 2008, the European Columbus laboratory set sail for humanity’s new world of space - join us live as we celebrate 10 years of achievements and look ahead to the future of human exploration ",
"Flexing our robotic muscles💪. A new robotic arm – that could be used to assemble spacecraft & future outposts for humans in space – was successfully tested to demonstrate that it is fully operational",
"Perfect timing -- down to the nanosecond -- is vital to navigation in deep space. More accurate timing = More control. For 20 years, we’ve been “perfecting time” for future deep space exploration. The result? The Deep Space Atomic Clock",
"Europe prepares to celebrate 10 years of its Columbus lab module at the space station as the crew studies the impacts of living in space",
# drones
"Ever fly in a cave? Check out these pilots putting in laps underground!",
"I think this pilot needs more batteries...How many do you bring to the field?",
"This drone is built for tricks! What do you think about seeing Freestyle in MultiGP?",
"Hey everyone hope you have an awesome time at the 2018 Sebring Drone Race presented by Soaring Sky. Here's what we have planned for today! ",
"An army of Racing Drones, getting ready to FLY!!!",
"Jordan Temkin (@jet.fpv) showing his drone racing skills here in Sebring 2018 day 1!!! ",
# games
"We've opened up a public Upcoming Beta branch on Steam so our most eager of Trailmakers can check out upcoming patches! Check out the notes and a tease of more news soon here! ",
"Hey guys! We’re hearing reports that Humble have revoked some of the pre-order keys, we’re not sure why but if you log into your Humble account, go to Purchases and activate the key from there again you’ll get Trailmakers back on your Steam account! Sorry about this!",
"We've deployed a small update with some critical fixes to Trailmakers! Read the notes",
"Build any vehicle you can dream up, and race it around an alien planet. This is for you grease monkeys. Trailmakers is coming out on Wednesday! ",
"Did you pre-order Trailmakers? We just sent you an e-mail asking what name/nickname you want us to put on - THE MONUMENT!",
"We're seeing a lot of feedback coming in from people playing the 10 month old Alpha demo. We love your feedback, but we'd love it even more if you were trying the new Alpha 2. Trailmakers should look like this in your Steam List if you're on the right build!"
]


def get_tf(text):
	terms = re.findall('(?u)\w+',text.lower())
	tf = Counter(terms)
	return dict(tf)

docs = list(map(get_tf,documents))

K = 3

topic_by_d_w = {}
cnt_by_t_w = {t:{} for t in range(1,K+1)}

# INIT
for d,doc in enumerate(docs):
	topic_by_d_w[d] = {}
	for w in doc:
		t = randint(1,K)
		topic_by_d_w[d][w] = t		
		if w not in cnt_by_t_w[t]: cnt_by_t_w[t][w]=0
		tf = doc[w]
		cnt_by_t_w[t][w] += tf

# ITER
for d,doc in enumerate(docs):
	for t in range(1,K+1):
		total_t = sum(cnt_by_t_w[t].values())
		cnt_in_t = sum([doc[w] for w in doc if topic_by_d_w[d][w]==t])
		for w in doc:
			p = cnt_by_t_w[t].get(w,0) / total_t * cnt_in_t
			print(d,t,w,p)
		