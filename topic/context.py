from collections import Counter

## def get_before(tab,i,cnt=1):
	## return tab[max(0,i-cnt):i]

## def get_after(tab,i,cnt=1):
	## return tab[i+1:i+1+cnt]

## # 15/s
## def get_context(tokens, cnt):	
	## before = {}
	## after = {}
	## tf = Counter()
	## for i,t in enumerate(tokens):
		## b = get_before(tokens, i, cnt)
		## if b:
			## if t not in before: before[t] = Counter()
			## before[t].update(b)
		
		## a = get_after(tokens, i, cnt)
		## if a:
			## if t not in after: after[t] = Counter()
			## after[t].update(a)
		
		## tf.update([t])
	
	## return dict(tf), {t:dict(b) for t,b in before.items()}, {t:dict(a) for t,a in after.items()}

# 92s
def get_context1(tokens):
	before = {}
	after = {}
	tf = {}
	for b,t,a in zip(['']+tokens,tokens,tokens[1:]+['']):
		if t not in tf:
			tf[t]=0
			before[t]={}
			after[t]={}
		tf[t] += 1
		if b: before[t][b] = before[t].get(b,0)+1
		if a: after[t][a] = after[t].get(a,0)+1
	return tf,before,after


# 71/s
from collections import defaultdict
def get_context2(tokens):
	before = defaultdict(lambda:defaultdict(int))
	after = defaultdict(lambda:defaultdict(int))
	tf = defaultdict(int)
	t=b=''
	for a in tokens+['']:
		tf[t] += 1
		before[t][b] += 1
		after[t][a] += 1
		b=t
		t=a
	return tf,before,after
