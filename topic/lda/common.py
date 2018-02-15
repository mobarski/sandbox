# encoding: utf8

import re
from random import random
from collections import Counter
from heapq import nlargest

from analyze import sentences_iter

DOCUMENTS = [
"reksio szczeka na koty",
"pies glosno szczeka",
"koty cicho mrucza",
"reksio to madry pies",
"kerbale buduja rakiety",
"rakiety wynosza satelity",
"satelity sa na orbicie",
"rakiety glosno startuja",
"szybowce leca cicho",
"szybowce startuja z wyciagarki",
"samoloty szturmowe leca nisko",
"krowy jedza trawe",
"kury jedza ziarno",
"krowy pija wode"
]

STOPWORDS = set(re.findall('(?u)\w+',u"""
	oraz gdzie jako jest tego jego przez jednak przy nich jeszcze nawet kiedy
	tylko siebie temu mnie natomiast tych sobie przed podczas bardzo
	już który też może które która jeżeli jeśli żeby także niż których którym której którego został
	się również którzy był było jeśli być będzie będą albo były właśnie którą była więc choć ktoś
	swój miał mogą czyli swoje kilka trochę nigdy więcej mniej
	mimo jestem jednym należy chociaż skoro masz między bardziej zwłaszcza jakiś
	wcześniej później mają można poza innych według dzięki swoich
	powinien chodzi takich tuż coraz czym swoim 
a
aby
ach
acz
aczkolwiek
aj
albo
ale
alez
ależ
ani
az
aż
bardziej
bardzo
beda
bedzie
bez
deda
będą
bede
będę
będzie
bo
bowiem
by
byc
być
byl
byla
byli
bylo
byly
był
była
było
były
bynajmniej
cala
cali
caly
cała
cały
ci
cie
ciebie
cię
co
cokolwiek
cos
coś
czasami
czasem
czemu
czy
czyli
daleko
dla
dlaczego
dlatego
do
dobrze
dokad
dokąd
dosc
dość
duzo
dużo
dwa
dwaj
dwie
dwoje
dzis
dzisiaj
dziś
gdy
gdyby
gdyz
gdyż
gdzie
gdziekolwiek
gdzies
gdzieś
go
i
ich
ile
im
inna
inne
inny
innych
iz
iż
ja
jak
jakas
jakaś
jakby
jaki
jakichs
jakichś
jakie
jakis
jakiś
jakiz
jakiż
jakkolwiek
jako
jakos
jakoś
ją
je
jeden
jedna
jednak
jednakze
jednakże
jedno
jego
jej
jemu
jesli
jest
jestem
jeszcze
jeśli
jezeli
jeżeli
juz
już
kazdy
każdy
kiedy
kilka
kims
kimś
kto
ktokolwiek
ktora
ktore
ktorego
ktorej
ktory
ktorych
ktorym
ktorzy
ktos
ktoś
która
które
którego
której
który
których
którym
którzy
ku
lat
lecz
lub
ma
mają
mało
mam
mi
miedzy
między
mimo
mna
mną
mnie
moga
mogą
moi
moim
moj
moja
moje
moze
mozliwe
mozna
może
możliwe
można
mój
mu
musi
my
na
nad
nam
nami
nas
nasi
nasz
nasza
nasze
naszego
naszych
natomiast
natychmiast
nawet
nia
nią
nic
nich
nie
niech
niego
niej
niemu
nigdy
nim
nimi
niz
niż
no
o
obok
od
około
on
ona
one
oni
ono
oraz
oto
owszem
pan
pana
pani
po
pod
podczas
pomimo
ponad
poniewaz
ponieważ
powinien
powinna
powinni
powinno
poza
prawie
przeciez
przecież
przed
przede
przedtem
przez
przy
roku
rowniez
również
sam
sama
są
sie
się
skad
skąd
soba
sobą
sobie
sposob
sposób
swoje
ta
tak
taka
taki
takie
takze
także
tam
te
tego
tej
ten
teraz
też
to
toba
tobą
tobie
totez
toteż
totobą
trzeba
tu
tutaj
twoi
twoim
twoj
twoja
twoje
twój
twym
ty
tych
tylko
tym
u
w
wam
wami
was
wasz
wasza
wasze
we
według
wiele
wielu
więc
więcej
wlasnie
właśnie
wszyscy
wszystkich
wszystkie
wszystkim
wszystko
wtedy
wy
z
za
zaden
zadna
zadne
zadnych
zapewne
zawsze
ze
zeby
zeznowu
zł
znow
znowu
znów
zostal
został
żaden
żadna
żadne
żadnych
że
żeby
"""))

def get_documents(multi=1):
	#documents = DOCUMENTS
	documents = sentences_iter('onet_text.mrl',20)
	docs = list(map(get_tf,documents))
	return docs*multi

def get_words(docs):
	words = set()
	for doc in docs:
		words.update(doc)
	return words

def get_tf(text):
	terms = re.split('[\s,.;():!?]+',text.lower())
	terms = [t for t in terms if len(t)>=4 and t.decode('utf8') not in STOPWORDS]
	tf = Counter(terms)
	return dict(tf)

def weighted_choice(w_map):
	items = w_map.items()
	cum_weights = [0]*len(items)
	cum_weights[0] = items[0][1]
	for i,item in enumerate(items):
		if i==0: continue
		w = item[1]
		cum_weights[i] = cum_weights[i-1]+w
	total = cum_weights[-1]
	r = random() * total
	for i,c in enumerate(cum_weights):
		if r<c: return items[i][0]


if __name__=="__main__":
	tf = Counter()
	for doc in get_documents():
		tf.update(doc)
	for x in nlargest(60,tf.items(),key=lambda x:x[1]):
		print x[0],x[1]
	for x in STOPWORDS:
		print(x.encode('utf8'))
	