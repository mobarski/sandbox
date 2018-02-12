from common import weighted_choice,get_documents,get_words

from pprint import pprint
from heapq import nlargest
from time import time
from random import randint

K = 6
ITERS = 1000
alpha = 0.1 # document alpha factor
eta = 0.1 # word eta factor
eta = 0.1 # word eta factor
MULTIPLICATION = 10

documents = get_documents(MULTIPLICATION)
words = get_words(documents)
topics = list(range(1,K+1))
docs = dict(enumerate(documents))

# INITIALIZE

t_wd = {w:{} for w in words}
n_dt = {d:{t:0 for t in topics} for d in docs}
n_wt = {w:{t:0 for t in topics} for w in words}
n_t = {t:0 for t in topics}
n_w = {w:0 for w in words} # DF

# randomly select topic for each word in each document
for d in docs:
	for w in docs[d]:
		t = randint(1,K)
		t_wd[w][d] = t
		n_dt[d][t] += 1
		n_wt[w][t] += 1
		n_t[t] += 1
		n_w[w] += 1

# MAIN LOOP
t0=time()
for _ in range(ITERS):
	for d in docs:
		#denom_dt = len(docs[d])-1 + K*alpha # denom_dt is not important
		for w in docs[d]:
			
			# decr current w/d/t
			t = t_wd[w][d]
			n_dt[d][t] -= 1
			n_wt[w][t] -= 1
			n_t[t] -= 1
			
			p_t = {}
			for t in topics:
				#denom_wt = n_w[w]-1 + K*eta # according to me (this can be moved to the outer loop)
				denom_wt = n_t[t] + K*eta # experimental
				#denom_wt = n_t[t] + len(words)*eta # according to _lda.pyx
				
				p_wt = 1.* (n_wt[w][t] + eta) / denom_wt
				p_dt = 1.* (n_dt[d][t] + alpha) # denom_dt is not important
				p_t[t] = p_wt * p_dt
				#print(denom_dt,denom_wt,p_wt,p_dt)

			# incr current w/d/t
			t = weighted_choice(p_t)
			t_wd[w][d] = t
			n_dt[d][t] += 1
			n_wt[w][t] += 1
			n_t[t] += 1
t1=time()

# RESULTS

for t in topics:
	top = nlargest(10,((w,n_wt[w][t]) for w in n_wt),key=lambda x:x[1])
	print('topic #{}  {}'.format(t,' '.join([x[0] for x in top if x[1]>0])))

print('{0:.2f} iters per second'.format(ITERS/(t1-t0)))
