from __future__ import print_function

# TODO normalize X
# TODO NN
# TODO transformacja tf-idf
# TODO transformacja log(TF)
# TODO KNN zamiast cosine_similarity

# DONE dict of METHOD specific arguments
# DONE PMI
# DONE NPMI = PMI w zakresie -1 do 1 -> slabo dziala
# DONE log(PMI)
# DONE normalizacja,standaryzacja
# DONE inne odleglosci zamiast cosine_similarity -> slabo dziala

# WNIOSKI:
# - rozne metody dekompozycji zaczynaja dzialac dobrze przy roznym progu N
# - lepsze wyniki dostaje sie gdy zbalansuje sie dane wejsciowe

# ---[ INPUT ]------------------------------------------------------------------

DOCUMENTS = [
"mezczyzna monarcha to krol",
"kobieta monarcha to krolowa",
"mlody kobieta to dziewczyna",
"mlody mezczyzna to chlopak",
"krolowa siedziec na tron",
"krol siedziec na tron",
"tron to krzeslo monarcha",
"monarcha siedziec na tron",
"poddani klekac przed krol",
"poddani klekac przed krolowa",

"mezczyzna i kobieta to plec",
"dawniej dziewczyna ubierac niebieski sukienka",
"teraz dziewczyna ubierac rozowy sukienka",
"dawniej chlopak ubierac rozowy koszula",
"teraz chlopak ubierac niebieski koszula",
"chlopak siedziec na krzeslo",
"dziewczyna siedziec na krzeslo",

"warszawa to stolica polska",
"paryz to stolica francja",
"moskwa to stolica rosja",
"polska to kraj",
"francja to kraj",
"rosja to kraj",
"paryz to miasto w francja",
"warszawa to miasto w polska",
"poznan to miasto w polska",
"torun to miasto w polska",
"moskwa to miasto w rosja",

"szef tesla to elon musk",
"elon musk to szef spacex",
"szef amazon to jeff bezos",
"szef facebook to mark zuckerberg",
"firma tesla produkowac samochod",
"firma spacex produkowac rakieta",
"firma amazon sprzedawac ksiazka",

"chlopak lubic rakieta",
"chlopak lubic samochod",
]

STOPWORDS = ['to','na','i','przed','w','byc']

# ---[ co-occurrence ]----------------------------------------------------------

import numpy as np
import re
from collections import Counter
from math import log

docs = [re.findall('(?u)\w+',doc) for doc in DOCUMENTS]
docs = map(lambda tokens:[t for t in tokens if t not in set(STOPWORDS)],docs)

co_cnt = Counter()
words = Counter()
for doc in docs:
	for i in range(len(doc)):
		w1 = doc[i]
		co_cnt[w1,w1] += 1 # DIAGONAL
		words[w1] += 1
		for j in range(i+1,len(doc)):
			w2 = doc[j]
			co_cnt[w1,w2] += 1
			co_cnt[w2,w1] += 1
word_by_id = dict(enumerate(sorted(words)))
id_by_word = {w:i for i,w in word_by_id.items()}

co_occ = np.zeros([len(words),len(words)])
for (w1,w2),cnt in co_cnt.items():
	i1 = id_by_word[w1]
	i2 = id_by_word[w2]
	co_occ[i1,i2] = cnt

# ---[ PMI - pointwise mutual information ]-------------------------------------

pair_norm = sum(sum(co_occ))
word_norm = sum(words.values())

pmi = np.zeros_like(co_occ)
chi = np.zeros_like(co_occ)
npmi = np.zeros_like(co_occ)-1
for (w1,w2),w1w2_cnt in co_cnt.items():
	i1 = id_by_word[w1]
	i2 = id_by_word[w2]
	w1_cnt = words[w1]
	w2_cnt = words[w2]
	nominator = 1.0 * w1w2_cnt / pair_norm
	denominator = (1.0 * w1_cnt / word_norm) * (1.0 * w2_cnt / word_norm) 
	pmi[i1,i2] = nominator / denominator
	# https://stats.stackexchange.com/questions/140935/how-does-the-logpx-y-normalize-the-point-wise-mutual-information
	npmi[i1,i2] = log(denominator) / log(nominator) - 1.0
	observed = w1w2_cnt
	expected = 1.0 * w1_cnt/word_norm * w2_cnt/word_norm * word_norm
	chi[i1,i2] = (observed - expected)**2 / expected

log_pmi = np.log(pmi+1)
log_chi = np.log(chi+1)
chi_pow = chi**0.33

# ---[ word vectors ]-----------------------------------------------------------

from sklearn.decomposition import PCA # H in range(-1,1)
from sklearn.decomposition import NMF # NO range limit
from sklearn.decomposition import IncrementalPCA as IPCA # H in range(-1,1)
from sklearn.decomposition import KernelPCA as KPCA # NO range limit
from sklearn.decomposition import TruncatedSVD as TSVD # H in range(-1,1)
from sklearn.decomposition import FactorAnalysis as FA # H in range(-1,1)
from sklearn.decomposition import SparsePCA as SPCA # W in range(-1,1)
from sklearn.decomposition import FastICA as ICA # W,H in range(-1,1)
from sklearn.decomposition import LatentDirichletAllocation as LDA # W in range(0,1)
from sklearn.decomposition import MiniBatchSparsePCA as MBSPCA # W in range(-1,1)
from sklearn.decomposition import MiniBatchDictionaryLearning as MBDL # H in range(-1,1)
from sklearn.decomposition import DictionaryLearning as DL # H in range(-1,1)

from sklearn.neural_network import MLPRegressor as NN
from sklearn.neural_network import BernoulliRBM as BRBM
from sklearn.manifold import TSNE

# ##############################################################################
# ###  KNOBS  ##################################################################
# ##############################################################################

VERBOSE = 0 # 0,1,2,3,4
X = log_pmi # log_pmi  chi_pow  co_occ  log_chi  chi  pmi  npmi
REDUCE = 1
N = 20
METHOD = PCA

# ##############################################################################
# ##############################################################################
# ##############################################################################

ARGS = { \
	NMF:{'max_iter':1000,'alpha':0.5},
	NN:{'max_iter':1000,'alpha':0.001,'activation':'identity','hidden_layer_sizes':[N]},
	BRBM:{'n_iter':1000,'learning_rate':0.03},
	TSNE:{'method':'exact'}
}

args = ARGS.get(METHOD,{})

if METHOD==NN:
	model = METHOD(**args)
	model.fit(X,X)
	print(model.loss_)
	print(model.n_iter_)
	W = model.coefs_[0]
else:
	model = METHOD(N,**args)
	W = model.fit_transform(X)

# select matrix where values are limited to -1,1 range
if METHOD in [SPCA,LDA,MBSPCA,KPCA,NN,TSNE]:
	V = W
else:
	H = model.components_
	V = H.transpose()
if not REDUCE:
	V = X

def get_word_vector(w):
	return V[id_by_word[w]].copy() # !!! musi byc copy !!!

# ---[ explain ]----------------------------------------------------------------

from heapq import nlargest,nsmallest

np.set_printoptions(threshold='nan',linewidth=130)

VT = np.around(V,1) # !!! V truncated to one decimal place

# words
if VERBOSE>=3:
	print()
	for i,v in enumerate(VT):
		vector = " ".join(map(lambda x:'{:2}'.format(int(x*(10 if REDUCE else 1))),v)).replace('0',".")
		print('{:20} {}'.format(word_by_id[i],vector))

# dimensions
if VERBOSE>=3:
	print()
	all_words = [x[1] for x in sorted(word_by_id.items())]
	for i in range(N):
		v = VT[:,i]
		by_weight = zip(v,all_words)
		hi = nlargest(4,by_weight)
		lo = nsmallest(4,by_weight)[::-1]
		hi = ['{}'.format(x[1]) for x in hi if x[0]]
		lo = ['{}'.format(x[1]) for x in lo if x[0]]
		print('dim','{:2}'.format(i+1),'-->',', '.join(hi),'...',', '.join(lo))

# ---[ similarity ]-------------------------------------------------------------

from sklearn.metrics.pairwise import cosine_similarity

def _similar(v,omit=[],n=0,verbose=0):
	if verbose>=2:
		#vector = ' '.join(map(lambda x:'{:5.2f}'.format(x),list(V[i])))
		vector = ' '.join(map(lambda x:'{:2d}'.format(int(x*(10 if REDUCE else 1))),list(v))).replace('0','.')
		print('      TARGET                  '+vector)
		print()
	
	omit_ids = set([id_by_word[w] for w in omit])
	cs = cosine_similarity([v],V)
	similarity = sorted(enumerate(cs[0]),key=lambda x:x[1],reverse=True)
	
	out = []
	cnt = 0
	for i,s in similarity:
		if n and cnt>=n: break
		if s>0 and i not in omit_ids:
			out += [(word_by_id[i],s)]
			if verbose:
				#vector = ' '.join(map(lambda x:'{:5.2f}'.format(x),list(V[i])))
				vector = ' '.join(map(lambda x:'{:2d}'.format(int(x*(10 if REDUCE else 1))),list(V[i]))).replace('0','.') if verbose>=2 else ''
				print("      {:15} {:.3f}   {}".format(word_by_id[i],s,vector))
			cnt += 1
	return out

ok_cnt=0
all_cnt=0
def similar(positive,negative='',expect=''):
	global ok_cnt
	global all_cnt
	print('# +',positive)
	if negative: print('# -',negative)
	if expect: print('# ==>',expect)
	
	pos = re.findall('(?u)\w+',positive)
	neg = re.findall('(?u)\w+',negative)
	omit = pos+neg
	v = get_word_vector(pos[0])
	for w in pos[1:]:
		v += get_word_vector(w)
	for w in neg:
		v -= get_word_vector(w)
	out = _similar(v,omit,6,verbose=VERBOSE)
	if expect:
		expected = expect.split(' ')
		expected_cnt = len(expected)
		best = set([x[0] for x in out[:expected_cnt]])
		ok = True
		for x in expected:
			if x not in best:
				ok = False
				break
		ok_cnt += 1 if ok else 0
		all_cnt += 1
		print('# OK' if ok else '# ERROR: '+' '.join([x[0] for x in out]))
		print()
		return ok

print()
similar('krol kobieta','mezczyzna','krolowa')
similar('monarcha siedziec','','tron')
#similar('dziewczyna chlopak','kobieta','samochod')

similar('stolica','','moskwa paryz warszawa')
similar('stolica polska','','warszawa')
similar('paryz rosja','francja','moskwa')
similar('kraj','','francja rosja polska')
similar('miasto','polska','moskwa paryz')

similar('szef tesla','','elon musk')
similar('szef bezos','','jeff amazon')
similar('bezos zuckerberg','amazon','facebook')

print()
print('OK -> {}/{} = {:.0f}%'.format(ok_cnt,all_cnt,100.*ok_cnt/all_cnt))


if VERBOSE>=4:
	import matplotlib.pyplot as plt
	from sklearn.manifold import TSNE
	p = TSNE(2).fit_transform(V)
	px = [x[0] for x in p]
	py = [x[1] for x in p]
	for x,y,w in zip(px,py,all_words):
		plt.scatter(x,y)
		plt.annotate(w,xy=(x,y))
	plt.show()
