from __future__ import print_function

# ---[ co-occurrence ]----------------------------------------------------------

# TODO transformacja tf-idf
# TODO transformacja log(TF)
# TODO regulacja -> [all]+=0.5
# TODO KNN zamiast cosine_similarity


# DONE PMI
# DONE NPMI = PMI w zakresie -1 do 1
# DONE log(PMI)
# DONE normalizacja,standaryzacja
# DONE inne odleglosci zamiast cosine_similarity -> slabo dziala

# WNIOSKI:
# - rozne metody dekompozycji zaczynaja dzialac dobrze przy roznym progu N
# - lepsze wyniki dostaje sie gdy zbalansuje sie dane wejsciowe

import numpy as np
import re
from collections import Counter
from math import log

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
## "paryz to miasto",
## "warszawa to miasto",
## "poznan to miasto",
## "torun to miasto",
## "moskwa to miasto",
## "paryz byc w francja",
## "warszawa byc w polska",
## "poznan byc w polska",
## "torun byc w polska",
## "moskwa byc w rosja",

"szef tesla to elon musk",
"szef amazon to jeff bezos",
"szef facebook to mark zuckerberg",
#"szef spacex to elon musk",
#"firma tesla produkowac samochod",
#"firma spacex produkowac rakieta",
#"firma amazon sprzedawac ksiazka",
] # TODO szef -> krol,ceo,tesla,amazon

STOPWORDS = ['to','na','i','przed','w','byc']


docs = [re.findall('(?u)\w+',doc) for doc in DOCUMENTS]
docs = map(lambda tokens:[t for t in tokens if t not in set(STOPWORDS)],docs)

co_occ = Counter()
words = Counter()
for doc in docs:
	for i in range(len(doc)):
		w1 = doc[i]
		co_occ[w1,w1] += 1 # DIAGONAL
		words[w1] += 1
		for j in range(i+1,len(doc)):
			w2 = doc[j]
			co_occ[w1,w2] += 1
			co_occ[w2,w1] += 1
word_by_id = dict(enumerate(sorted(words)))
id_by_word = {w:i for i,w in word_by_id.items()}

## print(id_by_word)

co_occ_arr = np.zeros([len(words),len(words)])
for (w1,w2),cnt in co_occ.items():
	i1 = id_by_word[w1]
	i2 = id_by_word[w2]
	co_occ_arr[i1,i2] = cnt

from sklearn.preprocessing import normalize
from sklearn.preprocessing import scale

##co_occ_arr += 0.5 # regulation
#co_occ_arr = scale(co_occ_arr)
#co_occ_arr = normalize(co_occ_arr)
#print(co_occ_arr)

# ---[ PMI - pointwise mutual information ]-------------------------------------

pair_norm = sum(sum(co_occ_arr))
word_norm = sum(words.values())

pmi = np.zeros_like(co_occ_arr)
chi = np.zeros_like(co_occ_arr)
npmi = np.zeros_like(co_occ_arr)-1
for (w1,w2),w1w2_cnt in co_occ.items():
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

np.set_printoptions(threshold='nan',linewidth=130)
#print(co_occ_arr.astype(int))
#print(chi.astype(int))

# ---[ word vectors ]-----------------------------------------------------------

from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD as TSVD
from scipy.sparse.linalg   import svds as SVDS
from sklearn.decomposition import FactorAnalysis as FA
from sklearn.decomposition import SparsePCA as SPCA
from sklearn.decomposition import FastICA as ICA
from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation as LDA
#from sklearn.decomposition import MiniBatchSparsePCA as MBSPCA
#from sklearn.decomposition import MiniBatchDictionaryLearning as MBDL
#from sklearn.decomposition import DictionaryLearning as DL

N = 20
#X = co_occ_arr
X = log_pmi
#X = chi
#X = npmi
#X = pmi
METHOD = PCA
VERBOSE = 0

if METHOD==SVDS:
	W,s,H = METHOD(X,N)
	W *= s
	H = (H.transpose()*s).transpose() # TODO optimize
else:
	model = METHOD(N)
	W = model.fit_transform(X)
	H = model.components_
if 1:
	V = W
elif 0:
	V = H.transpose()
else: # USE INPUT
	V = X

V = np.around(V,1) # !!!!!!!!!!!!!!!!!!!!!!!!!!!
# print(V)

def get_word_vector(w):
	return V[id_by_word[w]].copy() # !!! musi byc copy !!!

# explain
for w in []:
	v = get_word_vector(w)
	print('{:10} {}'.format(w,v.astype(int)))

# ---[ similarity ]-------------------------------------------------------------

from sklearn.metrics.pairwise import cosine_similarity

def _similar(v,omit=[],n=0,verbose=0):
	if verbose>=2:
		#vector = ' '.join(map(lambda x:'{:5.2f}'.format(x),list(V[i])))
		vector = ' '.join(map(lambda x:'{:2d}'.format(int(x)),list(v))).replace('0','.')
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
				vector = ' '.join(map(lambda x:'{:2d}'.format(int(x)),list(V[i]))).replace('0','.') if verbose>=2 else ''
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
		expected = expect.split(',')
		expected_cnt = len(expected)
		best = set([x[0] for x in out[:expected_cnt]])
		ok = True
		for x in expected:
			if x not in best:
				ok = False
				break
		ok_cnt += 1 if ok else 0
		all_cnt += 1
		print('# OK' if ok else '# ERROR -> '+','.join([x[0] for x in out]))
		print()
		return ok

print()
similar('monarcha kobieta','mezczyzna','krolowa')
similar('mlody mezczyzna','kobieta','chlopak')
similar('monarcha siedziec','','tron')
similar('stolica polska','','warszawa')
similar('stolica francja','','paryz')
similar('stolica','','moskwa,paryz,warszawa')
similar('kraj','','francja,rosja,polska')
#similar('miasto','','moskwa,warszawa,torun,poznan,paryz')
similar('miasto','polska','moskwa,paryz')
similar('szef tesla','','elon,musk')
similar('szef bezos','','jeff,amazon')
#similar('chlopak ubierac teraz','','koszula,niebieski') # TODO koszula,niebieski ok ale rozowy za wysoko

print()
print('OK -> {}/{} = {:.0f}%'.format(ok_cnt,all_cnt,100.*ok_cnt/all_cnt))
