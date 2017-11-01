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
freq = KV('data/freq')
t0=time()
tf_agg = Counter()
df_agg = Counter()
b_agg = {}
a_agg = {}
i = 0
for urlid,(tf,before,after) in freq.items():
	tf_agg.update(tf)
	df_agg.update(tf.keys())
	## for t,tf2 in before.items():
		## if t not in b_agg: b_agg[t] = Counter()
		## b_agg[t].update(tf2)
	## for t,tf2 in after.items():
		## if t not in a_agg: a_agg[t] = Counter()
		## a_agg[t].update(tf2)
	i += 1

## for k,v in tokens.items():
	## print(k)
	## tf,tfb,tfa = get_context1(v.split(' '))
	## tf_agg.update(tf)
	## for t,tfx in tfb.items():
		## if t not in tfb_agg: tfb_agg[t] = Counter()
		## tfb_agg[t].update(tfx)
	## for t,tfx in tfa.items():
		## if t not in tfa_agg: tfa_agg[t] = Counter()
		## tfa_agg[t].update(tfx)
	## i += 1
KV('data/tf').clear().update(tf_agg).sync()
KV('data/df').clear().update(df_agg).sync()
## KO('data/tfb').update({t:dict(tfx) for t,tfx in b_agg.items()}).sync()
## KO('data/tfa').update({t:dict(tfx) for t,tfx in a_agg.items()}).sync()
print(i/(time()-t0)) # tf_agg-only:302/s +before:41/s +after:23/s
