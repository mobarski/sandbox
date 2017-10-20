from collections import Counter

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

