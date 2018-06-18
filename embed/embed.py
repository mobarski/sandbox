from __future__ import print_function

# ---[ co-occurrence ]----------------------------------------------------------

# TODO transformacja tf-idf
# TODO transformacja log(TF)
# TODO regulacja -> [all]+=0.5
# TODO KNN zamiast cosine_similarity

# DONE normalizacja,standaryzacja
# DONE inne odleglosci zamiast cosine_similarity -> slabo dziala

# WNIOSKI:
# - rozne metody dekompozycji zaczynaja dzialac dobrze przy roznym progu N
# - lepsze wyniki dostaje sie gdy zbalansuje sie dane wejsciowe

import numpy as np
import re
from collections import Counter

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
"szef amazon to jeff bezos",
"szef facebook to mark zuckerberg",
#"szef spacex to elon musk",
#"firma tesla produkowac samochod",
#"firma spacex produkowac rakieta",
#"firma amazon sprzedawac ksiazka",
] # TODO szef -> krol,ceo,tesla,amazon

STOPWORDS = ['to','na','i','przed','w']


docs = [re.findall('(?u)\w+',doc) for doc in DOCUMENTS]
docs = map(lambda tokens:[t for t in tokens if t not in set(STOPWORDS)],docs)

co_occ = Counter()
words = set([''])
for doc in docs:
	for i in range(len(doc)):
		w1 = doc[i]
		co_occ[w1,w1] += 1 # ???
		words.add(w1)
		for j in range(i+1,len(doc)):
			w2 = doc[j]
			words.add(w2)
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

# ---[ word vectors ]-----------------------------------------------------------

from sklearn.decomposition import NMF
from sklearn.decomposition import PCA
from sklearn.decomposition import SparsePCA as SPCA
from sklearn.decomposition import MiniBatchSparsePCA as MBSPCA
from sklearn.decomposition import FactorAnalysis as FA
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.decomposition import TruncatedSVD as TSVD
from sklearn.decomposition import FastICA as ICA
from sklearn.decomposition import MiniBatchDictionaryLearning as MBDL
from sklearn.decomposition import DictionaryLearning as DL
from scipy.sparse.linalg   import svds as SVDS

N = 20

if True:
	model = PCA(N)
	W = model.fit_transform(co_occ_arr)
	H = model.components_
else:
	W,s,H = SVDS(co_occ_arr,N)
	W *= s
	H = (H.transpose()*s).transpose() # TODO optimize
if 0:
	V = W
elif 0:
	V = H.transpose()
else:
	V = co_occ_arr

#V = np.around(V,2)
#print(V)

def get_word_vector(w):
	return V[id_by_word[w]]

# explain
for w in []:
	v = get_word_vector(w)
	print('{:10} {}'.format(w,v.astype(int)))

# ---[ similarity ]-------------------------------------------------------------

from sklearn.metrics.pairwise import cosine_similarity

def _similar(v,omit=[],n=0):
	omit_ids = set([id_by_word[w] for w in omit])
	cs = cosine_similarity([v],V)
	similarity = sorted(enumerate(cs[0]),key=lambda x:x[1],reverse=True)
	
	print()
	cnt = 0
	for i,s in similarity:
		if n and cnt>=n: break
		if s>0 and i and i not in omit_ids:
			print(word_by_id[i],s)
			cnt += 1

def similar(positive,negative=''):
	pos = re.findall('(?u)\w+',positive)
	neg = re.findall('(?u)\w+',negative)
	omit = pos+neg
	v = get_word_vector(pos[0])
	for w in pos[1:]:
		v += get_word_vector(w)
	for w in neg:
		v -= get_word_vector(w)
	_similar(v,omit,6)

#similar('monarcha kobieta','mezczyzna') # -> krolowa
#similar('mlody mezczyzna','kobieta') # -> chlopak
#similar('krzeslo monarcha') # -> tron
#similar('stolica polska') # -> warszawa
#similar('stolica francja') # -> paryz
similar('kraj') # -> francja,rosja,polska
#similar('miasto','polska kraj') # -> moskwa,paryz
#similar('stolica') # -> moskwa,paryz,warszawa,,francja,polska,rosja
#similar('szef tesla') # elon,musk
#similar('szef bezos') # jeff,amazon
#similar('chlopak ubierac teraz') # TODO
