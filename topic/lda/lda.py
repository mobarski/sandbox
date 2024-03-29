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

K = 3

cnt_by_w_t = {} # cnt_by_w_t['test'] = {1:2,2:5,3:1}
t_in_doc = {} # t_in_doc[d] = {1:2,2:5,3:1}

def get_tf(text):
	terms = re.findall('(?u)\w+',text.lower())
	tf = Counter(terms)
	return dict(tf)

docs = list(map(get_tf,documents))

# INIT
for d,doc in enumerate(docs):
	t_in_doc[d] = {}
	for w in doc:
		#print(d,w)
		t = randint(1,K)
		# word
		if w not in cnt_by_w_t: cnt_by_w_t[w]={}
		if t not in cnt_by_w_t[w]: cnt_by_w_t[w][t]=0
		cnt_by_w_t[w][t] += 1
		# doc
		if t not in t_in_doc[d]: t_in_doc[d][t] = 0
		t_in_doc[d][t] += 1
# ITER
for d,doc in enumerate(docs):
	cnt_in_doc = sum(t_in_doc[d].values())
	for w in doc:
		cnt_in_topic = sum(cnt_by_w_t[w].values())
		for t in range(1,K+1):
			x1 = t_in_doc[d].get(t,0) / cnt_in_doc
			x2 = cnt_by_w_t[w].get(t,0) / cnt_in_topic
			print(w,t,x1,x2)
pprint(cnt_by_w_t)
pprint(t_in_doc)
