from collections import Counter
import re

main_text = """
Test byc niefajny.
Python byc fajny.
Miki byc fajny.
Miki to moj syn.
Agnieszka byc fajny.
Szermierka byc fajny.
Szermierka to sport.
Agnieszka to moj zona.
Agnieszka lubic gra planszowa.
Miki lubic samochod.
""".strip().lower()

topic_text = """
Maciek lubic szermierka.
Maciek lubic Miki.
""".strip().lower()

main_tokens = re.findall('\w+',main_text)
topic_tokens = re.findall('\w+',topic_text)

## main_tf = Counter(main_tokens)
## topic_tf = Counter(topic_tokens)
## main_tc = sum(main_tf.values())
## topic_tc = sum(topic_tf.values())

## main_rf = {t:1.0*f/main_tc for t,f in main_tf.items()}
## topic_rf = {t:1.0*f/topic_tc for t,f in topic_tf.items()}

## pdf = {t:f/main_rf.get(t,0.5/main_tc) for t,f in topic_rf.items()}


def get_before(tab,i,cnt=1):
	return tab[max(0,i-cnt):i]

def get_after(tab,i,cnt=1):
	return tab[i+1:i+1+cnt]

def get_context(tokens, cnt):	
	before = {}
	after = {}

	for i,t in enumerate(tokens):
		b = get_before(tokens, i, cnt)
		if b:
			if t not in before: before[t] = Counter()
			before[t].update(b)
		##
		a = get_after(tokens, i, cnt)
		if a:
			if t not in after: after[t] = Counter()
			after[t].update(a)
	
	return before, after


###########
from pprint import pprint
b,a = get_context(main_tokens,1)
pprint(b)
pprint(a)

#print(limit(dict(a=1,b=2,c=0),1))
