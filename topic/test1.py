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

main_tf = Counter(main_tokens)
topic_tf = Counter(topic_tokens)
main_tc = sum(main_tf.values())
topic_tc = sum(topic_tf.values())

main_rf = {t:1.0*f/main_tc for t,f in main_tf.items()}
topic_rf = {t:1.0*f/topic_tc for t,f in topic_tf.items()}

pdf = {t:f/main_rf.get(t,0.5/main_tc) for t,f in topic_rf.items()}


def before(tab,i,cnt):
	return tab[max(0,i-cnt):i]

def after(tab,i,cnt):
	return tab[i+1:i+1+cnt]

tokens_before = {}
tokens_after = {}

for i,t in enumerate(topic_tokens):
	if t not in tokens_before: tokens_before[t] = Counter()
	if t not in tokens_after: tokens_after[t] = Counter()
	tokens_before[t].update(before(topic_tokens,i,2))
	tokens_after[t].update(after(topic_tokens,i,2))

print(tokens_before)
print(tokens_after)
