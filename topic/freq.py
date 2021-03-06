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

from context import get_context1 as get_context

from contrib import *
from time import time
## tokens = KV('data/tokens.db',5)
## freq = KV('data/freq.db',5)
tokens = KO('data/tokens')
freq = KV('data/freq')
freqa = KV('data/freqa')
freqb = KV('data/freqb')
t0=time()
i = 0
for k,v in tokens.items(): # k->urlid
	print(k)
	if True or k not in freq:
		tf,tfb,tfa = get_context(v.split(' '))
		freq[k] = tf
		freqa[k] = tfa
		freqb[k] = tfb
		i += 1
freq.sync()
freqa.sync()
freqb.sync()
print(i/(time()-t0))
