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

from context import get_context1

from contrib import *
from time import time
tokens = KV('data/tokens.db',5)
t0=time()
tf_agg = Counter()
tfb_agg = {}
tfa_agg = {}
i = 0
for k,v in tokens.items():
	print(k)
	tf,tfb,tfa = get_context1(v.split(' '))
	tf_agg.update(tf)
	for t,tfx in tfb.items():
		if t not in tfb_agg: tfb_agg[t] = Counter()
		tfb_agg[t].update(tfx)
	for t,tfx in tfa.items():
		if t not in tfa_agg: tfa_agg[t] = Counter()
		tfa_agg[t].update(tfx)
	i += 1
print(i/(time()-t0)) # 33/s
