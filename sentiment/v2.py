# encoding: utf8

# na podstawie:
# - twitter (2200k tweetow)
# - TODO http://exp.lobi.nencki.gov.pl/nawl-analysis
# - TODO Affective norms for 1,586 polish words (ANPW): Duality-of-mind approach
# - TODO Slownik polskich wyzwisk, inwektyw i okreslen pejoratywnych - Ludwik Stomma
# - TODO Slownik polskich przeklenstw i wulgaryzmow - Maciej Grochowski

import re
from HTMLParser import HTMLParser
html = HTMLParser()

# TODO - re do odfiltrowania

url_re = re.compile(u'(?u)http[s]?://[\w/.-]+[\w]')
usr_re = re.compile(u'(?u)@\w+')
tag_re = re.compile(u'(?u)#\w+')


negative = ur"""	
aborcja		aborc[jiy]			# 1043
absurd		absurd				# 1635
absurd		absurd\w+			# 1410
agentura	\bagentur			# 466 agent=232=FP
agresja		agres[^t]			# 2180
alimenty	alimen				# 53
alkoholik	alkoholik\w*			# 97
amoralny	amoraln				# 14
aparatczyk	aparatczyk\w*			# 36
areszt		\b(za|)areszt			# 1865
arogancki	arogan				# 753
awantura	awantur\w*			# 543
awaria		\bawar[jiy]			# 234
babsztyl	babszt\w+			# 52
bac		\bbo(j[ęe]|imy)				# TODO 4240 bałem
badziew		badziew\w*			# 94
bagno		bag(ie)?n			# 725
bajzel		bajz[e]?l\w*			# 38
balagan		ba[łl]agan\w*			# 766
balwan		ba[łl]wan			# 29
bambus		bambus\w*			# FP
banda		\bband(a|y|dzie)\b		# 510
bandyta		\bbandy[ct]			# 528
bankrut		bankru[tc]			# 249
bankster	bankster\w*			# 74
baran		baran\w*			# 388 FP
barbarzynca	barbarz				# 161
bat		\bbat(|a|em|u|y)\b		# 207
becki		b[ęc]c[e]?k[i]?			# 12
bekart		b[ęe]kar[tc]			# 22
bestialski	bestial\w*			# 111
bezbronny	bezbron				# 55
bezcelowy	bezcel				# 6
bezczelny	bezczel				# 605
bezczescic	bezcze[śs]			# 31
bezduszny	bezdusz				# 24
bezmozg		bezm[óo]zg\w*			# 75
beznadzieja	beznadz\w+			# 791
bezradny	bezrad				# 84
bezsilny	bezsil				# 97
bezwartosciowy	bezwarto			# 110
biadolic	\bbiado				# 60
bieda		bied[ayno]			# 2881
biurwa		biurw\w*			# 2
blad		b[łl][ąaęe]d			# błędnik
blazen		b[łl]a[zź][e]?n			# 147
blizna		blizn				# 386
bojkot		bojkot\w*			# 513
bolszewia	bolszew\w*			# 791
bomba		bomb(?!el|oni)			# 1180
brak		brak				# 9193
brodawki	brodaw[e]?k			# 0
brud		brud(\b|[neo]\w*)		# 1041
brutalny	brutaln				# 259
brzydki		brzyd\w*			# 7237 +obrzyd
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
cherlawy	herlaw				# 3
chlac		\w*hlej|hla[cć]\w*		# 103
cholera		choler				# 4123
chory		chor[zaeouy]\w*			# 6087 choreo
chuj		chuj\w+				# 5077
chwast		hwast				# 58
ciapaty		ciapat\w+			# 22
cierpiec	cierpi				# 1410
ciota		\bciot\w+			# 290 ciotka ciotecz
cipa		\bcip\w*			# 187
ciul		ciul\w*				# 193
cpun		\b[ćc]pun\w*			# 31
cuchnie		cuchn\w+			# 75
cwel		cwel\w*				# 131
cynik		\bcyni\w+			# 182
cynik		cyni(k|cz|zm)			# 181
czarnuch	czarnuch\w*			# 10
czyhac		czyha				# 15
czystki		\bczyst[e]?k			# 65
daremny		daremn				# 40
dawn		\bd[ao][łlw]n(a|em|ach|om|owi)\b	# 1182 TODO dawny dawno dawni dawna
debil		debil\w*			# 3172
deficyt		deficyt				# 100
degeneracja	degener\w+			# 646
dekiel		dek(iel|lem|la|lu|le)\b		# 96
demagog		demagog\w*			# 87
demaskowac	demask\w+			# 155
denerwowac	denerw				# 2513
dluznik		(?<!po)d[łl]u[żz]n[iy](\b|[kc])	# 16
dno		\bdno\w*			# 703
dokuczac	dokucz				# 145
donos		donos\w*				# 1038 FP
donosiciel	donosicie			# 177
dopalacz	dopalacz			# 162
dramat		dramat				# 1127
draznic		dra[żz]n			# 107
dreczyc		\b[u]?dr[ęe]cz			# 79
dupa		\w*dup\w*			# 8323
durny		durn\w+				# 1020
dusic		(\b|u|przy|pod|za)du(si|sz[aąeęo])	# 1962 FP dusza
dyktator	dyktat[ou]r\w*			# 
dyletant	dyleta				# 9
dymac		dyma[ćclł]\w*			# 123
dziad		dziad(|[^ek]|[^ek]\w+)\b	# 1244 dziadek dziadkowie
dziwka		dziw[e]?k			# 264
dzuma		d[żz]um				# 81
egoista		egoi				# 105
elektrowstrzasy	elektrows			# 3
elyta		elyt\w*				# 65
embargo		embarg				# 21
endek		ende[ck]\w*			# 62 czy moze byc obrazliwe?
esbek		\besbe\w*			# 80
eunuch		eunuch				# 6
facjata		facja\w+			# 24
faszyzm		faszy[sz]			# 751
fatalny		fataln				# 445
fejk		fejk\w*				# 1178
fekalia		fekal\w*			# 21
fircyk		fircyk\w*			# 12
flak		fla(k(?![oer])|cz)		# 69
fortel		fortel				# 3
frajer		frajer\w*			# 522
fujara		fujar\w*			# 29
gach		\bgach\w*			# 45
gadula		\bgadu[lł]\w*			# 4
garb		garb\w+				# 111 garbarnia
gbur		gbur\w+				# 5
geba		g[ęe]b[eayio]\w*		# 467 spongebob
getto		\bgett(|o|a|cie|ach|om)\b	# 97
gimby		gimb\w+				# 280
gluchy		g[łl]uch\w+			# 410
glupi		g[łl]up\w+			# 7826
gnebic		gn[ęe]bi			# 88
gnic		gni([ćc]|[łl]\w*)\b		# 96
gnida		gnid\w*				# 174
gniew		gniew				# 627
gniot		gniot\w*			# 452
gnoj		gn[oó]j\w+			# 488
gorszy		gorsz\w+			# 9542
gorzki		gorzk				# 288
gowno		g[oó]wn\w+			# 3761
grob		gr[óo]b				# 871
groteska	grotesk\w+			# 96
grozic		gr[óo](zi|[źżz])		# 
gruby		grub\w+				# 1435
gulag		gu[łl]ag\w*			# 49
gwalt		gwa[łl]t(?!own)			# 253
halas		\bha[łl]a[sś]			# 99
hanba		ha[ńn]b\w*			# 624
haniebny	hanieb				# 264
hazard		hazard				# 108
herezja		here[zt]			# 50
hipokryta	hipokry\w+			# 668
hitler		hitler\w*			# 390
hochsztapler	hochsztapl\w+			# 2211
holocaust	holo[ck]a			# 989
holota		ho[łl]o[tc]			# 1521
horda		\bhord				# 35
horror		horror				# 247
hucpa		hucp				# 437
idiota		\bidio\w+			# 3147
ignorant	ignoran[tc]\w*			# 293
incydent	incydent			# 56
indoktrynacja	indoktryn			# 32
intryga		intryg(?!uj|ow)			# 68
irytuje		iryt\w+				# 1733
japa		\bjap[aąeęyi](\b|[^n]|[^n]\w+)		# TODO japonia japierdole
jebac		jeba\w+				# 12359 -> jeb,zjeb,jebi itp
jelen		jele[ńn]\w*			# FP
jelop		je[łl]op\w*			# 86
judzic		judz[ia][ćc]			# 14
kablowac	(?<!o)kabl(uj|owa[ćcłl])	# 13
kaftan		kaftan(?!ik)			# 48
kaganiec	kaga(ni|[ńn]c)			# 121
kajdanki	kajdan				# 379
kal		\bka([ł]|le)\w*				# TODO kałuża
kanalia		kanali\w*			# 288
kanibal		kanibal				# 21
kapitulacja	kapitul([^yea]\b|\w\w)		# 52 kapituła
kapus		kapu[śs](\b|[iuó]\w*)		# 35
karalny		karaln				# 205
karaluch	karaluch			# 28
karierowicz	karierowicz\w*			# 26
katastrofa	katastrof			# 1031
katol		katol(\b|i\b|[ea]\w*)		# 152
katowac		\b(|s|za)katow(?!ic)		# 360
katusze		katusz				# 42
kibol		kibo\w*				# 762
kicz		\bkicz				# 68
kiepski		kiepsk				# 373
kila		\bki[łl](a|e|ę|y|om)\b		# 83 FP
klamca		(?<!re)k[łl]am\w*		# 4625 klamke klamka
klapa		klap[aynlłi]			# 142
kloaka		kloa[ck]\w*			# 10
klocic		k[łl][óo][tc](\b|[^k])		# 1296
klozet		klozet\w*			# 6
knebel		kneb(el|lo|li)			# 26
knur		knur\w*				# 32
kochanek	kochan([e]?k|ic)		# 155
kolaborant	kolabor\w+			# 398
kolchoz		ko[łl][c]?hoz\z*		# 73
komornik	komornik			# 165
komplikacje	komplik				# 293
kompromitacja	kompromit			# 1206
komuch		komuch\w+			# 397
komunizm	komuni[sz]			# 1816
koncentracyjny	koncentracy			# 153
kondolencje	kondolenc			# 22 FP
konflikt	konflikt			# 634
konus		konus\w*			# 946
kopnac		kopn\w+				# 481 kopac
korupcja	koru(mpo|pcj)			# 299
koszmar		koszmar				# 549
kpic		\bkpi				# 302
kradl		krad[łlzn]\w*			# 3313
kretacz		kr[ęe]tac\w+			# 103
kretyn		\bkrety\w+			# 817
krew		kr(ew\b|wi|waw)			# 3151
kryminal	krymina[łl]			# 3568
krytyczny	krytycz				# 269
krytyk		krytyk				# 2153
kryzys		kryzys				# 580
krzyk		krzy(k|cz)			# 4328
krzywda		\w*krzywd\w+			# 1297
kuglarz		kuglar\w+			# 47
kukla		kuk[łl]				# 53
kulawy		\bkul(aw|ej)\w+			# 86
kundel		kund[e]?l\w*			# 253
kuper		\bkup[e]?r\w*			# 43
kurupcja	korupc\w+			# 203
kurwa		(ku|q)rw\w+			# 43737
kustykac	(?<!a)ku[śs]ty			# 19
kutas		kuta\w+				# 749
kłamca		kłam\w+				# 3499
lajdak		[lł]ajda\w+			# 45
lament		\blament			# 224
lapowka		\b[łl]ap[óo]w\w*		# 241
lekkomyslny	lekkomy				# 5
leming		lem[m]?in\w+			# 706
len		\ble(ń|ni)\w*			# 1912 lenin
lenin		lenin\w*			# 237
lewak		lewa[ck]\w*			# 2851
lewatywa	lewatyw				# 32
lgac		\b[ł](ga|[żz]e)\w*		# 109
libacja		libac[jk]\w+			# 38
lobby		lobb				# 594
loch		\bloch(\b|u|[óo]w|em|ami)		# TODO lochy (swinie)
lubiezny	lubie[żz]n\w+			# 6
ludobojstwo	ludob[óo]j			# 512
lupic		\b(z|roz|)[łl]upi[cćł]		# 14
lustrowac	\blustr(ow|ac)			# 11
lysy		\b[łl]ys\w+			# 359 wylysiec
macki		mac(ka|ki|ek|kom|kami)\b	# 73
maczeta		maczet				# 18
makabra		makabr				# 28
malaria		malari				# 2
malkontent	malkon				# 36
malwersacje	malwers				# 32
manipulacja	manipul\w+			# 1094
marks		marks\w*			# 934
martwy		martw(?!i[ećcłl])\w		# 1222
masakra		masakr\w*			# 1035
masochista	masochi[sz]			# 72 sado maso
maszkara	maszkar				# 4
matol		mato[łl]\w*			# 263
mdlosci		md[łl]o[śs]			# 39
meczyc		m[ęe]cz(ony|[ąa]c)			# TODO 870 meczach męczy-meczy
menda		\bmenda\w*				# TODO
miernota	miern\w*			# 
milicja		\bmilic				# 97
mocz		mocz(|u|em)\b			# 79
mogila		mogi[łl]			# 29
monotonia	monoton(?!icz)			# 40
monstrualny	\bmonstru			# 18
morda		mord\w*					# TODO 5372 morda i morderca
morderca	\bmorder			# 448
morderstwo	mord(er|ow)			# 2256
mordowac	\b(za|)mordow			# 1630
motloch		mot[łl]och\w*			# 100
murzynski	murzy[nń]\w*			# 323
nachalny	nachaln\w*			# 32
nagana		nagan(?!ia)			# 56
naiwny		naiwn\w+			# 534
napad		napad				# 301
napasc		napa(st|[śs][ćc])		# 1010
narkotyki	narko[tm]			# 337
naziol		nazi\w*				# 1001
negatywne	ne(gatywn|gacja|gow)		# 395
nekrofil	nekrofil			# 12
nicosc		nico[śs][ćc]			# 19
niebezpieczny	niebezp				# 703
niebyt		niebyt\w*			# 33
nieczuly	nieczu[lł]			# 105
niedopatrzenie	niedopat			# 13
niedorzeczny	niedorzeczn\w+			# 45
niedozwolony	niedozwol			# 22
niedzorzeczny	niedorze			# 45
nielaska	nie[łl]ask			# 10
nielegalny	nielegal			# 541
niemowa		\bniemow[^l]\w*			# 8
nienawisc	nienawi[dśs]			# 6168
nieporadny	nieporad			# 49
nieprawidlowy	nieprawi			# 478
nieprzyjazny	nieprzyja			# 7
niespawiedliwy	\bniespraw			# 296
niespokojny	niespoko			# 25
nieszczegolny	nieszczeg			# 6
nieszczescie	nieszcz[ęe][śs]			# 606
nietrzezwy	nietrze[źz]			# 17
nieuczciwy	nieuczc				# 48
nieudacznik	\bnieudaczni\w+			# 203
nieudacznik	nieudacz			# 212
nieufny		nieufn				# 183
nieuprawniony	nieupraw			# 12
niewdzieczny	niewdzi				# 57
niewierny	niewiern			# 46
niewolnik	niewolni			# 166
niewypal	niewypa[lł]			# 66
niezdrowy	niezdrow			# 105
niezgodny	niezgodn			# 193
niezyciowy	nie[żz]yci			# 2
niezywy		nie[żz]yw			# 22
niski		\bnisk\w+			# 802 niskoemisyjny
niszczyc	niszcz\w*			# 3281
niwygodny	niewygod			# 232
nowotwor	nowotw				# 204
nuklearny	nuklear				# 345
obawa		\bobaw				# 1305
obelga		obel[gżz]\w*			# 99
oblakany	ob[łl][ąa]kan			# 40
oblawa		ob[łl]aw			# 41
obled		ob[łl][ęd]d			# 148
oblesny		oble[sś]\w*			# 87 oblech
obskurny	obskur				# 5
obwisly		obwi[śs]			# 5
ochyda		ochyd\w+			# 129
odbyt		odby(t|ci)\w*			# 139 odbycia
odwet		odwet				# 108
odwyk		odwyk				# 42
ofiara		ofiar				# 3267
ograniczac	ogranicz			# 2550
ohyda		o[c]?hyd\w+			# 163
okrutny		okru[ct]			# 556
opium		opium				# 51
opozniony	(o|za)p[óo][źz]nion\w		# 75
oprych		opry(ch|szk)\w*			# 4
ordynardny	ordynar\w*			# 154
osiol		osio[łl]|osł[aeo]\w*		# TODO 
oslizgly	o[śs]liz[g]?[łl]y		# 27
oszolom		oszo[łl]om\w*			# 146
oszust		\boszu(st|k)\w*			# 2417
owdowiec	owdowi				# 0
pacjent		pacjen				# 429
pacyfikowac	pacyfik[aou]\w			# 263
padlina		padlin				# 36
pajac		pajac\w*			# 919
palic		pal(i[ćcłl]|on|[ąa]c)		# 3437
panika		pani(k|czn)			# 1183
paser		paser 				# 14
pasożyt		paso[żz]y			# 96
patologia	patol\w*			# 1573
pazerny		pazern\w+			# 155
pedal		peda[lł]			# 858
pederasta	peder\w+			# 85
pedofil		pedofil				# 334
penis		penis\w*			# 107
perwers		perwer\w*			# 163
pieklo		(\b|[^u])piek(ie)?[łl]		# 682
pieprzyc	piepr\w+			# 3183
pierdol		pierd\w+			# 19138
pionek		\bpion[e]?k			# 26
pirat		\b(anty|)pira[ct]		# 198
pisdu		pisd[auoy]\w*			# 224
pislam		pislam\w*			# 56
pisuar		pisuar\w*			# 42
pizda		pi[zź]d\w+			# 1446
placz		p[łl]a(cz|ka[^t])		# 10818
plaga		plag(?!ia)			# 117
plagiat		plagia				# 94
plebs		pleb[se]\w*			# 62
plesn		ple[śs][nń]			# 36 pleśnierowicz
pluskwa		pluskw\w*			# 14 FP
pochwa		pochw(a|y|om|[eę])\b		# 25
podczlowiek	pod(cz[łl]ow|lud)\w+		# 56
podstep		podst[ęe]p			# 385
podzegacz	pod[żz]eg			# 19
podły		pod[łl][ay]\w+			# 174
pogarda		\b(pogard|wzgard|gardz)		# 1460
pogrom		pogrom				# 342
pogrzeb		pogrzeb				# 1369
pogrzeb		pogrzeb				# 1369 FP
pokonac		pokon[ay]			# 628
pokuta		pokut				# 64
poligamia	poligam				# 32
ponury		ponur				# 170
porazka		pora[zż][e]?k			# 1068
poronic		poroni				# 22 poronin
posepny		pos[ęe]p			# 16
potwor		potw[óo]r			# 452 potwornie
pozar		po[żz]ar(\b|[^tlł])		# 503
prawak		prawa[kc]\w*			#
pregierz	pr[ęe]gierz			# 10
presja		presj				# 975
prl		peerel|\bprl			# 1345
problem		problem				# 11258
prochno		pr[óo]chn(?!ik)			# 22
profanowac	profan[aou]			# 81
propaganda	propagand\w*			# 2171
prostak		\bprosta\w+			# 388
prostytucja	prostytu			# 117
protest		prote[śs]			# 10381
prymityw	prymityw\w*			# 485
pryszcz		pryszcz\w*			# 291
przegrac	przegr[ay]			# 3737
przemoc		przemoc				# 939
przepasc	przepa[śs][ćc]			# 220
przestepca	przest[ęe]p[^oni]		# 1732
przygnebiony	przygn[ęe]b			# 52
przykrosc	przykro[śs][ćc]			# 52
przykry		przykr(y|ym|ych|ymi|o|e|ego)\b	# 2523
przymus		przymus				# 392
psychol		psych\w+			# 3951 psycholog psychika
pulapka		pu[łl]apk			# 107
pustka		\bpustk				# 893
puszczalski	puszczals\w+			# 7
pysk		pysk\w*				# 758 FP	
pyskowac	pysk(at|[oó]w|uj)		# 60
rabowac		rabowa\w+			# 88
rabunek		rabun[e]?k\w*			# 105
radykal		radyka[łl]			# 332
ranic		(\b|z)rani[ćcłlo]		# 1058
ranny		\brann				# 157 FP
retard		retard\w*			# 40
rezygnacja	rezygn				# 1058
roszczenia	\broszcz[ye]			# 1342
rozczarowac	rozczarow\w+			# 721
rozgardiasz	rozgardiasz			# 11
rozpacz		rozpacz\w*			# 607
rozwiazly	rozwi[ąa]z[łl]\w+		# 11
rozwod		rozw[óo]d			# 113
ruchac		rucha\w*			# 1572
ruina		ru[ij]n\w*			# 598 FP
rusek		rus(ek|cy|ki|ka|ko)		# 2192
ryj		\bryj\w*			# 3871
rzez		\brze[źz](\b|n|i)		# 191
rzygac		rzyg\w*				# 9158 przygladac przygotowac
sabotowac	sabot				# 174
sadlo		\bsad[łl][oae]\w*		# 20 sadlok
sadysta		sady[sz]			# 41 sado maso
samobojca	samob[óo]j			# 698
samotny		samotn				# 648
sarkazm		sarka[sm]			# 61
sciek		\b[śs]ciek(\b|[^a])		# 70
scierwo		[śs]cierw\w*			# 454
sekta		\bsek(t(?!or)|ci)		# 239 sektor sekciarski sekcja insekt
sidla		(?<!roman)sid[e]?[łl]			# 22 TODO
sierota		siero[tc]			# 412
sierp		sierp(\b|[^in])			# 51
skandal		skandal				# 2339
skarzyc		skar[żzg]			# 2610
skostnialy	skostnia			# 9
slaby		s[lł]ab\w+			# 5978
slepy		[śs]lep\w+			# 607
slina		(\b|za|po|ob|wy)[śs]li[nń]		# 150
smieci		[śs]mie[cć](|[^h]|[^h]\w+)\b	# 853
smierc		[śs]mier[ćct]			# 5727
smierdzi	[śs]mierd\w+			# 652
smietnik	[śs]mietni\w+			# 183
smrod		smr[óo]d\w*			# 201
smutek		smut\w+				# 7207
snob		snob				# 15
socjalizm	socjali				# 607
sodomia		sodom[ia]			# 16
spam		spam\w*				# 3074
spisek		spis[e]?k			# 628
spoliczkowac	spoliczko			# 3
sprzeciw	sprzeciw			# 333
sprzeczny	sprzecz				# 462
sral		sra[^cłlłnmj]\w+			# TODO 1444 -> sra
srom		srom\w*				# 41
ssman		\b[e]?s[e]?sman\w*		# 5
stagnacja	stagn				# 18
stalin		stalin\w*			# 459
strach		stra(ch|sz)			# 7230
strajk		strajk\w*			# 371
strup		\bstrup				# 7
sucz		sucz[yoeęaą]?\b			# 27
suka		\bsuk(|i|ą|om|ami|in\w+)\b	# 308
swietokradztwo	[śs]wi[ęe]tokrad		# 15
swinia		[śs]wi[ńn]\w*			# 1808 -> swinoujscie
swir		[śs]wir\w+			# 505
swolocz		swo[łl]oc\w+			# 71
syf		syf\w*					# 683 TODO syfon klasyfikacja intensyfikacja
syfilis		syfili[sz]			# 6
syjonista	syjo(nis|[ńn]sk)		# 174
szajs		szajs\w+			# 163
szambo		szamb\w+			# 1292
szantaz		szanta[żz]			# 189
szatan		s[z]?atan			# 296
szczac		\b(|wy|ze|za|o|po)szcz(a\b|a[^w]|yn)	# 138 szczaw
szczuc		szczu[ćcjlł]\w+			# mieszczuch?
szczur		szczur\w*			# 2004 FP
szelma		szelm				# 0
szkalowac	szkal				# 444
szkielet	szkielet			# 33
szmalcownik	szmalcow\w+			# 116
szmata		szma[ct]\w*			# 2139
szmira		\bszmir				# 14
szok		szok				# 3038
szpieg		szpieg				# 206
szubienica	szubien				# 256
szuja		\bszuj\w*			# 78
szumowina	szumowin\w*			# 50
szwab		szwab\w*			# 339
szydzic		szydz\w+			# 213
szykany		szykan				# 288
tandeta		tandet\w+			# 53
tchorz		tch[óo]rz\w*			# 1303
tepy		t[ęe]p[yaei]			# 2133
terror		terror\w*			# 1010
tlusty		t[łl]u[śs]			# 361
toksyczny	toksy				# 166
tortury		tortur				# 292
totalitarny	totali				# 90
totalny		totaln				# 3351 totalnie
tragiczny	tragi[cz]			# 787
trauma		traum				# 258
troll		\w*trol\w*				# 3384 TODO kontrola patrol controll
truc		tru(ci[zce]|[łlt][ayoi])		# TODO 157 truly(ANG) trucizna vs truc
truchlo		truch[lł]			# 33
trudno		\btrudn[oiay]			# 3151
trumna		trum(ie)?n			# 247
trup		\btrup				# 335
tylek		ty[łl](ek|ka|ecz)\w*		# 1534
tyran		tyra[nń]				# 57 TODO tyranie tyraniu
ubek		\bube[ck]\w*			# 241
ublizac		ubli[żz]\w+			# 111
ujma		\bujm[ay]			# 8
ulom		u[łl]om\w+			# 97
umarly		umar[łl]			# 1191
umierac		umier				# 2536
unicestwic	unicest				# 23
utytlany	\w*tyt[łl]a\w*			# 2
uzurpator	uzurp\w+			# 25
wampir		wampir				# 674
warchol		warcho\w+			# 46
wariat		wari(a[ct]|owa)\w*		# 614
wariat		wari(at|ow|uj)			# 628
weto		(\b|za|po)[wv]eto		# 641
wieloryb	wieloryb\w*			# 35
wiezienie	wi[ęe]zie[nń]			# 1302
wirus		wirus				# 318
wojna		woj[e]?n			# 9550
wojownik	woj[oó]w			# 251
wol		\bw[oó]ł(|u|y|em|owi|owe|owa|ami)\b	# 39
wredny		wredn\w+			# 1283
wrogi		wr[óo]g				# 2535
wrzeczec	wrzeszcz			# 138
wscibski	w[śs]cib			# 9
wsciekly	w[śs]ciek			# 482
wsciekly	w[śs]ciek\w+			# 481
wstret		wstr[ęe]t			# 146
wstret		wstr[ęe]t\w*			# 146
wstyd		wstyd\w*			# 3176
wszy		wsz(on|aw|y\b)\w+		# 25
wtargnac	\bwtarg				# 31
wyc		\b(za|roz|)wy([ćc]|je\w*|[łl](|y|i|i[śs]\w+))\b		# TODO wychowanie wychodzic wycofac wyciag wycieczka
wykroczenie	wykrocz[^n]			# 47
wyludzic	wy[łl]udz			# 1705
wymiotowac	wymio[ct][^lł]			# 337
wypadek		wypad[e]?k			# 2556
wyrzutek	wyrzut[e]?k			# 6
zabic		zabi[cćtj]			# 3917
zabojstwo	zab[óo]j\w			# 423
zabor		zab[óo]r			# 67
zachlanny	zach[łl]ann			# 59
zadluzony	zad[łl]u[żz]			# 140
zadufany	zaduf				# 22
zagazowac	zagazo				# 11
zakaz		zakaz				# 2797
zakladnik	zak[łl]adni			# 146
zalamac		za[łl]am[ak]			# 527
zalamac		za[łl]am\w+			# 752
zaloba		\b[żz]a[łl]ob			# 95
zalosc		\b[żz]a[łl]o[sś]\w+		# 2101
zalosny		[żz]a[łl]o[sś][cćn]\w*		# 2219
zamach		zamach\w*			# 1995 zamachowski
zaminowac	\b(pod|za)minow[au]		# 0
zaorac		\b(za|prze|wy|roz|)ora[ćcłln]	# 1093
zaraza		zaraz[ayo]			# 168
zarazic		zara([źz][nl]|[żz][oa]|zi|zk)	# 180
zastoj		zast[óo]j			# 1
zatarg		\bzatarg			# 496
zawiesc		zaw(iod|ied|odz|ie[śs][ćc])	# 1385
zazdrosc	zazdro[sś][ncćz]		# 3270
zblazowany	zblazo				# 4
zboj		zb[óo]j\w*			# 130 zbojkotowac
zbrodnia	zbrodn				# 2220
zdrada		zdra[dj]			# 3773
zdychac		(?<!w)zdych			# 272
zdzira		zdzir				# 11
zebrac		żebra					# 152 TODO żebra(MED)
zenujacy	za[żz]eno|żenu			# 1502
zgielk		zgie[łl]k			# 24
zgon		(\b|ze)zgon			# 118
zgraja		\bzgraj[iao]			# 10
zl*		\b[źz][lł][eyoiaąu]\b			# TODO 9488 zly zle zlo zlymi zla
zlamas		z[łl]amas\w+			# 21
zlodziej	złodziej\w*			# 1920
zlosc		\bz[łl]o[śs]			# 693
zmarly		zmar[łl]			# 628
zmusic		zmus[zi]			# 1066
zoltek		[żz][óo]lt[e]?k\w*		# 1 FP
zombie		zombi				# 543
zoofil		zoofil				# 8
zul		żul\w*				# 167
zwalic		zwa[lł]\w*				# 4167 TODO rozwalic zwalic rozwalka walic
zwloki		zw[łl]ok(?![lłęe])		# 128
zwyrodnialy	zwyro[ld]			# 599
zydo		\b[żz]yd(k|o[^wm])		# 1047
"""
# zabójstwo ludobójstwo dreczyc zbrodnia pacyfikacja goj zgorzknialy wściekły
# łby wina drzeć złudzenia kulfon ograniczony groza zgryzota tyrać ból cierpieć
# zlom prosze (postawa roszczeniowa)
# odebrać zabrać zwłoki zmarł zczezł
# błąd zmęczenie psuć sprzeczac sprzeciw    mogiła nędza katorga mdlićd uszny targac
# żmija sęp leszcz locha loszka glizda
key = 'x'

pattern = {}
for line in negative.strip().split('\n'):
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

