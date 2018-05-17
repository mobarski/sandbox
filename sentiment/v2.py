# encoding: utf8

# zrodla:
# - twitter (2200k tweetow)
# - TODO http://exp.lobi.nencki.gov.pl/nawl-analysis
# - TODO ksiazka 1
# - TODO ksiazka 2

import re
from HTMLParser import HTMLParser
html = HTMLParser()

# TODO - re do odfiltrowania

url_re = re.compile(u'(?u)http[s]?://[\w/.-]+[\w]')
usr_re = re.compile(u'(?u)@\w+')
tag_re = re.compile(u'(?u)#\w+')


data = ur"""	
aborcja		aborc[jiy]			# 1043
absurd		absurd\w+			# 1410
agentura	\bagentur			# 466 agent=232=FP
alkoholik	alkoholik\w*			# 97
amoralny	amoraln				# 14
aparatczyk	aparatczyk\w*			# 36
awantura	awantur\w*			# 543
awaria		\bawar[jiy]			# 234
babsztyl	babszt\w+			# 52
bac		\bbo(j[ęe]|imy)				# TODO 4240 bałem
badziew		badziew\w*			# 94
bajzel		bajz[e]?l\w*			# 38
balagan		ba[łl]agan\w*			# 766
balwan		ba[łl]wan			# 29
bambus		bambus\w*			# FP
banda		\bband(a|y|dzie)\b		# 510
bandyta		\bbandy[ct]			# 528
bankster	bankster\w*			# 74
baran		baran\w*			# 388 FP
bat		\bbat(|a|em|u|y)\b		# 207
becki		b[ęc]c[e]?k[i]?			# 12
bestialski	bestial\w*			# 111
bezmozg		bezm[óo]zg\w*			# 75
beznadzieja	beznadz\w+			# 791
biadolic	\bbiado				# 60
bieda		bied[ayno]			# 2881
biurwa		biurw\w*			# 2
blad		b[łl][ąaęe]d			# błędnik
bojkot		bojkot\w*			# 513
bolszewia	bolszew\w*			# 791
brak		brak				# 9193
brud		brud(\b|[neo]\w*)		# 1041
brzydki		brzyd\w*			# 7237
burak		bura\w+				# 397
burza		burz				# 5491
bydlo		byd[łl]\w+			# 843
bylejak		bylejak				# 23
bzdura		bzdu\w+				# 962
bzdury		bzdur\w+			# 808
cenzura		cenz[uo]r			# 2339
chala		\bcha[łl]a			# 41
cham		\bcham[^p]\w+			# 2750
chaos		chao[st]			# 310
chlac		\w*hlej|hla[cć]\w*		# 103
chory		chor[zaeouy]\w*			# 6087 choreo
chuj		chuj\w+				# 5077
ciapaty		ciapat\w+			# 22
cierpiec	cierpi				# 1410
ciota		\bciot\w+			# 290 ciotka ciotecz
cipa		\bcip\w*			# 187
ciul		ciul\w*				# 193
cpun		\b[ćc]pun\w*			# 31
cuchnie		cuchn\w+			# 75
cwel		cwel\w*				# 131
cynik		\bcyni\w+			# 182
czarnuch	czarnuch\w*			# 10
czystki		\bczyst[e]?k			# 65
dawn		\bd[ao][łlw]n(a|em|ach|om|owi)\b	# 1182 TODO dawny dawno dawni dawna
debil		debil\w*			# 3172
degeneracja	degener\w+			# 646
demagog		demagog\w*			# 87
demaskowac	demask\w+			# 155
dno		\bdno\w*			# 703
donos		donos\w*				# 1038 FP
dupa		\w*dup\w*			# 8323
durny		durn\w+				# 1020
dyktator	dyktator\w*			# 116
dymac		dyma[ćclł]\w*			# 123
dziad		dziad(|[^ek]|[^ek]\w+)\b	# 1244 dziadek dziadkowie
elyta		elyt\w*				# 65
endek		ende[ck]\w*			# 62 czy moze byc obrazliwe?
esbek		\besbe\w*			# 80
eunuch		eunuch				# 6
facjata		facja\w+			# 24
faszyzm		faszy[sz]			# 751
fejk		fejk\w*				# 1178
fekalia		fekal\w*			# 21
fircyk		fircyk\w*			# 12
frajer		frajer\w*			# 522
fujara		fujar\w*			# 29
gach		\bgach\w*			# 45
gadula		\bgadu[lł]\w*			# 4
garb		garb\w+				# 111 garbarnia
gbur		gbur\w+				# 5
geba		g[ęe]b[eayio]\w*		# 467 spongebob
gimby		gimb\w+				# 280
gluchy		g[łl]uch\w+			# 410
glupi		g[łl]up\w+			# 7826
gnebic		gn[ęe]bi			# 88
gnic		gni([ćc]|[łl]\w*)\b		# 96
gnida		gnid\w*				# 174
gniot		gniot\w*			# 452
gnoj		gn[oó]j\w+			# 488
gorszy		gorsz\w+			# 9542
gowno		g[oó]wn\w+			# 3761
groteska	grotesk\w+			# 96
grozic		gro(zi|[źżz])			# 6363
gruby		grub\w+				# 1435
gulag		gu[łl]ag\w*			# 49
halas		\bha[łl]a[sś]			# 99
hanba		ha[ńn]b\w*			# 624
herezja		here[zt]			# 50
hipokryta	hipokry\w+			# 668
hitler		hitler\w*			# 390
hochsztapler	hochsztapl\w+			# 2211
holocaust	holo[ck]a			# 989
holota		ho[łl]o[tc]			# 1521
horda		\bhord				# 35
hucpa		hucp				# 437
idiota		\bidio\w+			# 3147
ignorant	ignoran[tc]\w*			# 293
indoktrynacja	indoktryn			# 32
irytuje		iryt\w+				# 1733
japa		\bjap[aąeęyi](\b|[^n]|[^n]\w+)		# TODO japonia japierdole
jebac		jeba\w+				# 12359 -> jeb,zjeb,jebi itp
jelen		jele[ńn]\w*			# FP
jelop		je[łl]op\w*			# 86
judzic		judz[ia][ćc]			# 14
kal		\bka([ł]|le)\w*				# TODO kałuża
kanalia		kanali\w*			# 288
kanibal		kanibal				# 21
kapus		kapu[śs](\b|[iuó]\w*)		# 35
karierowicz	karierowicz\w*			# 26
katol		katol(\b|i\b|[ea]\w*)		# 152
kibol		kibo\w*				# 762
kicz		\bkicz				# 68
klamca		(?<!re)k[łl]am\w*		# 4625 klamke klamka
klapa		klap[aynlłi]			# 142
kloaka		kloa[ck]\w*			# 10
klozet		klozet\w*			# 6
knur		knur\w*				# 32
kolaborant	kolabor\w+			# 398
kolchoz		ko[łl][c]?hoz\z*		# 73
komplikacje	komplik				# 293
komuch		komuch\w+			# 397
kondolencje	kondolenc			# 22 FP
konus		konus\w*			# 946
kopnac		kopn\w+				# 481 kopac
koszmar		koszmar				# 549
kradl		krad[łlzn]\w*			# 3313
kretacz		kr[ęe]tac\w+			# 103
kretyn		\bkrety\w+			# 817
krzywda		\w*krzywd\w+			# 1297
kuglarz		kuglar\w+			# 47
kulawy		\bkul(aw|ej)\w+			# 86
kundel		kund[e]?l\w*			# 253
kuper		\bkup[e]?r\w*			# 43
kurupcja	korupc\w+			# 203
kurwa		(ku|q)rw\w+			# 43737
kutas		kuta\w+				# 749
kłamca		kłam\w+				# 3499
lajdak		[lł]ajda\w+			# 45
lajdak		łajda\w+			# 41
lapowka		\b[łl]ap[óo]w\w*		# 241
leming		lem[m]?in\w+			# 706
len		\ble(ń|ni)\w*			# 1912 lenin
lenin		lenin\w*			# 237
lewak		lewa[ck]\w*			# 2851
lgac		\b[ł](ga|[żz]e)\w*		# 109
libacja		libac[jk]\w+			# 38
lubiezny	lubie[żz]n\w+			# 6
lupic		\b(z|roz|)[łl]upi[cćł]		# 14
lysy		\b[łl]ys\w+			# 359 wylysiec
manipulacja	manipul\w+			# 1094
marks		marks\w*			# 934
masakra		masakr\w*			# 1035
masochista	masochi[sz]			# 72 sado maso
matol		mato[łl]\w*			# 263
meczyc		m[ęe]cz(ony|[ąa]c)			# TODO 870 meczach męczy-meczy
menda		\bmenda\w*				# TODO
miernota	miern\w*			# 
mocz		mocz(|u|em)\b			# 79
morda		mord\w*				# 5372 morda i morderca
motloch		mot[łl]och\w*			# 100
murzynski	murzy[nń]\w*			# 323
nachalny	nachaln\w*			# 32
naiwny		naiwn\w+			# 534
naziol		nazi\w*				# 1001
negatywne	ne(gatywn|gacja|gow)		# 395
nekrofil	nekrofil			# 12
nicosc		nico[śs][ćc]			# 19
niebyt		niebyt\w*			# 33
niedorzeczny	niedorzeczn\w+			# 45
niemowa		\bniemow[^l]\w*			# 8
nieudacznik	\bnieudaczni\w+			# 203
niewierny	niewiern			# 46
niski		\bnisk\w+			# 802 niskoemisyjny
niszczyc	niszcz\w*			# 3281
obawa		\bobaw				# 1305
obelga		obel[gżz]\w*			# 99
oblakany	ob[łl][ąa]kan			# 40
obled		ob[łl][ęd]d			# 148
oblesny		oble[sś]\w*			# 87 oblech
ochyda		ochyd\w+			# 129
odbyt		odby(t|ci)\w*			# 139 odbycia
ohyda		o[c]?hyd\w+			# 163
okrutny		okru[ct]			# 556
opozniony	(o|za)p[óo][źz]nion\w		# 75
oprych		opry(ch|szk)\w*			# 4
ordynardny	ordynar\w*			# 154
osiol		osio[łl]|osł[aeo]\w*		# TODO 
oslizgly	o[śs]liz[g]?[łl]y		# 27
oszolom		oszo[łl]om\w*			# 146
oszust		\boszu(st|k)\w*			# 2417
padlina		padlin				# 36
pajac		pajac\w*			# 919
patologia	patol\w*			# 1573
pazerny		pazern\w+			# 155
pedal		peda[lł]			# 858
pederasta	peder\w+			# 85
pedofil		pedofil				# 334
penis		penis\w*			# 107
perwers		perwer\w*			# 163
pieprzyc	piepr\w+			# 3183
pierdol		pierd\w+			# 19138
pisdu		pisd[auoy]\w*			# 224
pislam		pislam\w*			# 56
pisuar		pisuar\w*			# 42
pizda		pi[zź]d\w+			# 1446
placz		p[łl]a(cz|ka[^t])		# 10818
plebs		pleb[se]\w*			# 62
pluskwa		pluskw\w*			# 14 FP
pochwa		pochw(a|y|om|[eę])\b		# 25
podczlowiek	pod(cz[łl]ow|lud)\w+		# 56
podły		pod[łl][ay]\w+			# 174
pogarda		\b(pogard|wzgard|gardz)		# 1460
pogrom		pogrom				# 342
pogrzeb		pogrzeb				# 1369 FP
pokonac		pokon[ay]			# 628
porazka		pora[zż][e]?k			# 1068
prawak		prawa[kc]\w*			#
presja		presj				# 975
problem		problem				# 11258
propaganda	propagand\w*			# 2171
prostak		\bprosta\w+			# 388
prymityw	prymityw\w*			# 485
pryszcz		pryszcz\w*			# 291
przegrac	przegr[ay]			# 3737
przemoc		przemoc				# 939
przepasc	przepa[śs][ćc]			# 220
psychol		psych\w+			# 3951 psycholog psychika
pustka		\bpustk				# 893
puszczalski	puszczals\w+			# 7
pysk		pysk\w*				# 758 FP	
rabowac		rabowa\w+			# 88
rabunek		rabun[e]?k\w*			# 105
retard		retard\w*			# 40
rozczarowac	rozczarow\w+			# 721
rozgardiasz	rozgardiasz			# 11
rozpacz		rozpacz\w*			# 607
rozwiazly	rozwi[ąa]z[łl]\w+		# 11
ruchac		rucha\w*			# 1572
ruina		ru[ij]n\w*			# 598 FP
rusek		rus(ek|cy|ki|ka|ko)		# 2192
ryj		\bryj\w*			# 3871
rzygac		rzyg\w*				# 9158 przygladac przygotowac
sadlo		\bsad[łl][oae]\w*		# 20 sadlok
sadysta		sady[sz]			# 41 sado maso
samobojca	samob[óo]j			# 698
scierwo		[śs]cierw\w*			# 454
skandal		skandal				# 2339
slaby		s[lł]ab\w+			# 5978
slepy		[śs]lep\w+			# 607
smieci		[śs]mie[cć](|[^h]|[^h]\w+)\b	# 853
smierdzi	[śs]mierd\w+			# 652
smietnik	[śs]mietni\w+			# 183
smrod		smr[óo]d\w*			# 201
smutek		smut\w+				# 7207
sodomia		sodom[ia]			# 16
spam		spam\w*				# 3074
sral		sra[^cłlłnmj]\w+		# 1444 -> sra
srom		srom\w*				# 41
ssman		\b[e]?s[e]?sman\w*		# 5
stalin		stalin\w*			# 459
strach		stra(ch|sz)			# 7230
strajk		strajk\w*			# 371
strup		\bstrup				# 7
sucz		sucz[yoeęaą]?\b			# 27
suka		\bsuk(|i|ą|om|ami|in\w+)\b	# 308
swinia		[śs]wi[ńn]\w*			# 1808 -> swinoujscie
swir		[śs]wir\w+			# 505
swolocz		swo[łl]oc\w+			# 71
syf		syf\w*					# 683 TODO syfon klasyfikacja intensyfikacja
syjonista	syjo(nis|[ńn]sk)		# 174
szajs		szajs\w+			# 163
szambo		szamb\w+			# 1292
szantaz		szanta[żz]			# 189
szczac		\b(|wy|ze|za|o|po)szcz(a\b|a[^w]|yn)	# 138 szczaw
szczuc		szczu[ćcjlł]\w+			# mieszczuch?
szczur		szczur\w*			# 2004 FP
szkalowac	szkal				# 444
szmalcownik	szmalcow\w+			# 116
szmata		szma[ct]\w*			# 2139
szmira		\bszmir				# 14
szuja		\bszuj\w*			# 78
szumowina	szumowin\w*			# 50
szwab		szwab\w*			# 339
szydzic		szydz\w+			# 213
tandeta		tandet\w+			# 53
tchorz		tch[óo]rz\w*			# 1303
tepy		t[ęe]p[yaei]			# 2133
terror		terror\w*			# 1010
totalitarny	totali				# 90
totalny		totaln				# 3351 totalnie
trauma		traum				# 258
troll		\w*trol\w*				# 3384 TODO kontrola patrol controll
truchlo		truch[lł]			# 33
trudno		\btrudn[oiay]			# 3151
trup		\btrup				# 335
tylek		ty[łl](ek|ka|ecz)\w*		# 1534
tyran		tyra[nń]				# 57 TODO tyranie tyraniu
ubek		\bube[ck]\w*			# 241
ublizac		ubli[żz]\w+			# 111
ujma		\bujm[ay]			# 8
ulom		u[łl]om\w+			# 97
utytlany	\w*tyt[łl]a\w*			# 2
uzurpator	uzurp\w+			# 25
warchol		warcho\w+			# 46
wariat		wari(a[ct]|owa)\w*		# 614
wariat		wari(at|ow|uj)			# 628
wieloryb	wieloryb\w*			# 35
wol		\bw[oó]ł(|u|y|em|owi|owe|owa|ami)\b	# 39
wredny		wredn\w+			# 1283
wrogi		wr[óo]g				# 2535
wsciekly	w[śs]ciek\w+			# 481
wstret		wstr[ęe]t\w*			# 146
wstyd		wstyd\w*			# 3176
wszy		wsz(on|aw|y\b)\w+		# 25
wyc		\b(za|roz|)wy([ćc]|je\w*|[łl](|y|i|i[śs]\w+))\b		# TODO wychowanie wychodzic wycofac wyciag wycieczka
wyludzic	wy[łl]udz			# 1705
zabor		zab[óo]r			# 67
zalamac		za[łl]am\w+			# 752
zaloba		\b[żz]a[łl]ob			# 95
zalosc		\b[żz]a[łl]o[sś]\w+		# 2101
zalosny		[żz]a[łl]o[sś][cćn]\w*		# 2219
zamach		zamach\w*			# 1995 zamachowski
zaorac		\b(za|prze|wy|roz|)ora[ćcłln]	# 1093
zastoj		zast[óo]j			# 1
zboj		zb[óo]j\w*			# 130 zbojkotowac
zdrada		zdra[dj]			# 3773
zenujacy	za[żz]eno|żenu			# 1502
zgielk		zgie[łl]k			# 24
zgraja		\bzgraj[iao]			# 10
zl*		\b[źz][lł][eyoiaąu]\b			# TODO 9488 zly zle zlo zlymi zla
zlamas		z[łl]amas\w+			# 21
zlodziej	złodziej\w*			# 1920
zlosc		\bz[łl]o[śs]			# 693
zoltek		[żz][óo]lt[e]?k\w*		# 1 FP
zoofil		zoofil				# 8
zul		żul\w*				# 167
zwalic		zwa[lł]\w*				# 4167 TODO rozwalic zwalic rozwalka walic
zydo		\b[żz]yd(k|o[^wm])		# 1047
x				
"""
# zabójstwo ludobójstwo dreczyc
# łby wina drzeć złudzenia kulfon ograniczony groza zgryzota tyrać ból cierpieć absurd
# zlom prosze (postawa roszczeniowa)
# odebrać zabrać zwłoki zmarł zczezł
# błąd zmęczenie psuć
key = 'x'

pattern = {}
for line in data.strip().split('\n'):
	rec = re.split('\t+',line.rstrip())
	pattern[rec[0]] = rec[1]

test_re = re.compile(pattern[key],re.U)

all = []
#f = open(r'C:\repo\twitter\reference_7d.tsv')
f = open(r'C:\repo\war_room\data\reference_7d.tsv')
for line in f:
	text = html.unescape(line.rstrip().split('\t')[-1].decode('utf8')).lower()
	text = tag_re.sub('#TAG',text)
	text = url_re.sub('#URL',text)
	text = usr_re.sub('#USER',text)
	m = test_re.findall(text)
	if m:
		print(text.encode('utf8'))
		all.extend(m)

print('')
print(len(all))

