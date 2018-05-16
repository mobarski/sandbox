# encoding: utf8

import re
from HTMLParser import HTMLParser
html = HTMLParser()

# TODO - re do odfiltrowania

url_re = re.compile(u'(?u)http[s]?://[\w/.-]+[\w]')
usr_re = re.compile(u'(?u)@\w+')
tag_re = re.compile(u'(?u)#\w+')


data = ur"""	
kurwa		(ku|q)rw\w+			# 43737
chuj		chuj\w+				# 5077
pizda		pi[zź]d\w+			# 1446
jebac		jeba\w+				# 12359 -> jeb,zjeb,jebi itp
pierdol		pierd\w+			# 19138
beznadzieja	beznadz\w+			# 791
glupi		g[łl]up\w+			# 7826
szambo		szamb\w+			# 1292
komuch		komuch\w+			# 397
sral		sra[^cłlłnmj]\w+		# 1444 -> sra
cham		\bcham[^p]\w+			# 2750
prostak		\bprosta\w+			# 388
nieudacznik	\bnieudaczni\w+			# 203
kretyn		\bkrety\w+			# 817
idiota		\bidio\w+			# 3147
durny		durn\w+				# 1020
bzdura		bzdu\w+				# 962
podły		pod[łl][ay]\w+			# 174
ochyda		ochyd\w+			# 129
kłamca		kłam\w+				# 3499
gnoj		gn[oó]j\w+			# 488
gowno		g[oó]wn\w+			# 3761
szajs		szajs\w+			# 163
pieprzyc	piepr\w+			# 3183
kutas		kuta\w+				# 749
ryj		\bryj\w*			# 3871
debil		debil\w*			# 3172
pajac		pajac\w*			# 919
burak		bura\w+				# 397
frajer		frajer\w*			# 522
szmata		szma[ct]\w*			# 2139
swinia		[śs]wi[ńn]\w*			# 1808 -> swinoujscie
miernota	miern\w*			# 
bolszewia	bolszew\w*			# 791
lajdak		łajda\w+			# 41
pedal		peda[lł]			# 858
pederasta	peder\w+			# 85
ciota		\bciot\w+			# 290 ciotka ciotecz
zalosc		\b[żz]a[łl]o[sś]\w+		# 2101
ruchac		rucha\w*			# 1572
rzygac		rzyg\w*				# 9158 przygladac przygotowac
lewak		lewa[ck]\w*			# 2851
prawak		prawa[kc]\w*			#
brzydki		brzyd\w*			# 7237
smierdzi	[śs]mierd\w+			# 652
oblesny		oble[sś]\w*			# 87 oblech
murzynski	murzy[nń]\w*			# 323
sucz		sucz\b				# 25
gbur		gbur\w+				# 5
wredny		wredn\w+			# 1283
irytuje		iryt\w+				# 1733
klamca		(?<!re)k[łl]am\w*		# 4625 klamke klamka
kradl		krad[łlzn]\w*			# 3313
zlodziej	złodziej\w*			# 1920
patologia	patol\w*			# 1573
konus		konus\w*			# 946
dno		\bdno\w*			# 703
scierwo		[śs]cierw\w*			# 454
gorszy		gorsz\w+			# 9542
slaby		s[lł]ab\w+			# 5978
psychol		psych\w+			# 3951 psycholog psychika
szczuc		szczu[ćcjlł]\w+			# mieszczuch?
elyta		elyt\w*				# 65
plebs		pleb[se]\w*			# 62
bzdury		bzdur\w+			# 808
lajdak		[lł]ajda\w+			# 45
badziew		badziew\w*			# 94
zalosny		[żz]a[łl]o[sś][cćn]\w*		# 2219
gimby		gimb\w+				# 280
rozczarowac	rozczarow\w+			# 721
niedorzeczny	niedorzeczn\w+			# 45
zalamac		za[łl]am\w+			# 752
cipa		\bcip\w*			# 187
gnida		gnid\w*				# 174
szuja		\bszuj\w*			# 78
dymac		dyma[ćclł]\w*			# 123
kibol		kibo\w*				# 762
kretacz		kr[ęe]tac\w+			# 103
ignorant	ignoran[tc]\w*			# 293
tchorz		tch[óo]rz\w*			# 1303
karierowicz	karierowicz\w*			# 26
x		o[śs]liz[g]?[łl]y		# 27
x		oszo[łl]om\w*			# 146
x		cwel\w*				# 131
x		ciul\w*				# 193
x		żul\w*				# 167
x		hochsztapl\w+			# 82
x		ende[ck]\w*			# 62
x		wari(a[ct]|owa)\w*		# 614
x		\boszu(st|k)\w*			# 2417
x		\bcyni\w+			# 182
x		prymityw\w*			# 485
x		pislam\w*			# 56
x		demagog\w*			# 87
x		ordynar\w*			# 154
x		nachaln\w*			# 32
x		\b[ł](ga|[żz]e)\w*		# 109
x		kuglar\w+			# 47
x		rabowa\w+			# 88
x		rabun[e]?k\w*			# 105
x		żydokom\w+			# 228
x		hipokry\w+			# 668
x		dyktator\w*			# 116
x		nazi\w*				# 1001
x		swo[łl]oc\w+			# 71
x		je[łl]op\w*			# 86
x		\b[ćc]pun\w*			# 31
x		obel[gżz]\w*			# 99
x		aparatczyk\w*			# 36
x		uzurp\w+			# 25
x		bankster\w*			# 74
x		szydz\w+			# 213
x		propagand\w*			# 2171
x		cuchn\w+			# 75
x		stalin\w*			# 459
x		hitler\w*			# 390
x		lenin\w*			# 237
x		marks\w*			# 934
x		warcho\w+			# 46
x		ubli[żz]\w+			# 111
x		kapu[śs](\b|[iuó]\w*)		# 35
x		\besbe\w*			# 80
x		mato[łl]\w*			# 263
x		\bkup[e]?r\w*			# 43
x		pisuar\w*			# 42
x		pisd[auoy]\w*			# 224
x		ha[ńn]b\w*			# 624
x		\bujm[ay]			# 8
x		\bmenda\w*			# TODO
x		\ble(ń|ni)\w*			# 1912 lenin
x		wstyd\w*			# 3176
x		szwab\w*			# 339
x		smr[óo]d\w*			# 201
x		grub\w+				# 1435
x		bajz[e]?l\w*			# 38
"""
key = 'x'

pattern = {}
for line in data.strip().split('\n'):
	rec = re.split('\t+',line.rstrip())
	pattern[rec[0]] = rec[1]

test_re = re.compile(pattern[key],re.U)

i = 0 
f = open(r'C:\repo\twitter\reference_7d.tsv')
for line in f:
	text = html.unescape(line.rstrip().split('\t')[-1].decode('utf8')).lower()
	text = tag_re.sub('#TAG',text)
	text = url_re.sub('#URL',text)
	text = usr_re.sub('#USR',text)
	m = test_re.findall(text)
	if m:
		print(text.encode('utf8'))
		i += 1

print(i)
