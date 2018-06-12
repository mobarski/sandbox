# encoding: utf8
from __future__ import print_function

# na podstawie:
# - twitter (2200k tweetow)
# - TODO http://exp.lobi.nencki.gov.pl/nawl-analysis
# - TODO Affective norms for 1,586 polish words (ANPW): Duality-of-mind approach
# - TODO Slownik polskich wyzwisk, inwektyw i okreslen pejoratywnych - Ludwik Stomma
# - TODO Slownik polskich przeklenstw i wulgaryzmow - Maciej Grochowski

import re
from HTMLParser import HTMLParser
html = HTMLParser()


from itertools import izip_longest
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

# TODO - re do odfiltrowania

url_re = re.compile(u'(?u)http[s]?://[\w/.-]+[\w]')
usr_re = re.compile(u'(?u)@\w+')
tag_re = re.compile(u'(?u)#\w+')

# GRUPA:
# [h]istoria
# [p]olityka/spoleczne
# [z]wierzeta -> [b]iologia
# [s]mutek + [ss]mierc
# [a]gresja/przemoc
# se[x]ualnosc
# [o]dchody/[o]draza/nieczystosci/rozklad/zepsucie/choroby/brud
# [i]nwektywa
# [d]yskryminacja / pogarda
# [w]ulgaryzm:
#    * w - pospolity wulgaryzm systemowy slabo nacechowany lub eufemizm wulgaryzmu systemowego
#    * ww - wulgaryzm systemowy
#    * www - wulgaryzm systemowy silnie nacechowany
#    ??? co z wulgaryzmami obyczajowymi?
# [r]eligia
# [m]medycyna
#
# odnosnie cech: [f]izycznych/wygladu, [u]myslowe, spolecznych/zachowania/behawioralnych
# bol, [c]ierpienie, strach
# wymiar sprawiedliwosci / [k]odeks karny / prawo

# klucz  tagi  wzorzec  notatki
negative = ur"""	
_			.		\bk(|u|ur)([*]+|[.][.]+)([aęeiy]|w[aęeiy])	# 206 k*rwa
aberracja		.		\baberr				# 14
absurd			.		absurd				# 1635
absurd			.		absurd\w+			# 1410
alienacja		.		alien(ow|ac)			# 4
alimenty		k		alimen				# 53
areszt			k		\b(za|)areszt			# 1865
atrapa			.		\batrap				# 105
awaria			.		\bawar[jiy]			# 234
bac			.		\bbo(j[ęe]|imy)				# TODO 4240 bałem
bac			.		\b(boj[ęe]|boisz|boi|boimy|boicie|boj[ąa]|b[óo]j|b[óo]jcie|ba[łl]em|ba[łl]am|ba[łl]o|bali[śs]my|ba[łl]y[śs]my|ba[łl]|ba[łl]a|ba[łl]o)\b		# 8402 TODO uproscic
badziew			.		badziew\w*			# 94
bajzel			.		bajz[e]?l\w*			# 38
balagan			.		ba[łl]agan\w*			# 766
balast			.		balast				# 17
banda			.		\bband(a|y|dzie)\b		# 510
bat			a		\bbat(|a|em|u|y)\b		# 207
bazgroly		.		bazgr[oa]			# 39
becki			.		b[ęc]c[e]?k[i]?			# 12
belkot			.		be[łl]ko[tc]			# 291
besztac			.		beszt				# 5
bezcelowy		.		bezcel				# 6
bezczelny		.		bezczel				# 605
bezczescic		.		bezcze[śs]			# 31
bezczynny		.		bezczyn				# 239
bezdenny		.		bezd[e]?n			# 16
bezdomny		.		bezdom				# 125
bezkarny		.		bezkar				# 357
bezmiar			.		bezmiar				# 44
bezmozg			mu		bezm[óo]zg\w*			# 75
beznadzieja		.		beznadz\w+			# 791
bezprawie		k		bezpraw				# 368
bezrobotny		.		bezrobo				# 181
bezsensowny		.		bezsens				# 379
beztalencie		u		beztalen			# 12
bezwartosciowy		.		bezwarto			# 110
biadolic		.		\bbiado				# 60
bieda			.		bied[ayno]			# 2881
bierny			.		biern				# 472
blad			.		\bbł[ąę]d				# TODO DUPLIKAT 2467
blad			.		b[łl][ąaęe]d				# TODO DUPLIKAT błędnik
bluzgac			.		bluzg				# 78
brak			.		brak				# 9193
brednie			.		\bbred[zn]			# 632
burda			.		burd([ayę]|\b)			# 50
bylejak			.		bylejak				# 23
bzdura			.		bzdu\w+				# 962
bzdury			.		bzdur\w+			# 808
cebula			.		cebul				# 345
chala			.		\bcha[łl]a			# 41
chaos			.		chao[st]			# 310
chlac			.		\w*hlej|hla[cć]\w*		# 103
chrzanic		.		chrzani				# 317
chwast			.		hwast				# 58
ciemnosc		.		ciemn				# 1499
cierpiec		.		cierpi				# 1410
czyhac			.		czyha				# 15
daremny			.		daremn				# 40
deficyt			.		deficyt				# 100
degeneracja		.		degener\w+			# 646
dekiel			.		dek(iel|lem|la|lu|le)\b		# 96
demaskowac		.		demask\w+			# 155
demotywowac		s		demotyw				# 2425
denerwowac		.		denerw				# 2513
dno			.		\bdno\w*			# 703
dokuczac		.		dokucz				# 145
donos			k		donos\w*				# TODO 1038 FP
dopalacz		.		dopalacz			# 162
dramat			.		dramat				# 1127
draznic			.		dra[żz]n			# 107
dreczyc			.		\b[u]?dr[ęe]cz			# 79
dusic			.		(\b|u|przy|pod|za)du(si|sz[aąeęo])	# TODO 1962 FP dusza
duszno			.		\bduszn				# 187
dyskomfort		.		(nie|dys)komfort		# 75
eksmisja		k		\b(wy|)eksmi[st]		# 10
ekstremalny		.		ekstrema			# 95
elyta			.		elyt\w*				# 65
facjata			f		facja\w+			# 24
falsz			.		fa[łl]sz			# 2893
fatalny			.		fataln				# 445
fejk			.		fejk\w*				# 1178
fikcja			.		fikc[y]?j			# 1514
flak			f		fla(k(?![oer])|cz)		# 69
fortel			.		fortel				# 3
garb			f		garb\w+					# TODO 111 garbarnia
geba			f		g[ęe]b[eayio]\w*			# TODO 467 spongebob
gimby			.		gimb\w+				# 280
gniot			.		\bgnio[tc](?![lł])		# 366
gniot			.		gniot\w*			# 452
gorszy			.		gorsz\w+			# 9542
gorzki			.		gorzk				# 288
granda			.		\bgrand(a|y)\b			# 14
groteska		.		grotesk\w+			# 96
gruby			f		grub\w+				# 1435
gruchot			f		gruchot				# 8
halas			.		\bha[łl]a[sś]			# 99
hanba			.		ha[ńn]b\w*			# 624
haniebny		.		hanieb				# 264
hazard			k		hazard				# 108
hejt			a		hejt				# 2844
histeria		.		hister				# 190
holota			.		ho[łl]o[tc]			# 1521
horda			.		\bhord				# 35
horror			.		horror				# 247
hucpa			.		hucp				# 437
incydent		.		incydent			# 56
infantylny		u		infantyl			# 24
intryga			.		intryg(?!uj|ow)			# 68
inwektywa		.		inwektyw			# 40
ironia			.		ironi				# 428
irytuje			.		iryt\w+				# 1733
jadrowy			.		j[ąa]drow			# 94
jaja			.		\bjaj				# 3302
japa			.		\bjap[aąeęyi](\b|[^n]|[^n]\w+)		# TODO japonia japierdole jajecznica
jeniec			.		\bje([ńn]c|nie)\w		# 61
judzic			.		judz[ia][ćc]			# 14
kablowac		.		(?<!o)kabl(uj|owa[ćcłl])	# 13
kaftan			m		kaftan(?!ik)			# 48
kantowac		.		kan(ciar|tow|tuj)			# TODO 20 krytykant
karalny			k		karaln				# 205
katorga			.		\bkator[gżz]				# TODO 24 lokatorzy
kicz			.		\bkicz				# 68
kiepski			.		kiepsk				# 373
klaki			.		\bk[łl]ak(?!ier)		# 54
klamot			.		klamot				# 0
klapa			.		klap[aynlłi]			# 142
kleska			.		\bkl[ęe]sk			# 245
klnac			.		\bkln				# 53
knebel			.		kneb(el|lo|li)			# 26
komornik		k		komornik			# 165
komplikacje		.		komplik				# 293
kompromitacja		.		kompromit			# 1206
kondolencje		s		kondolenc			# 22 FP
koryto			.		kory[tc](a\b|o|i)		# 364
koszmar			.		koszmar				# 549
kpic			.		\bkpi				# 302 KPI
kryminal		k		krymina[łl]			# 3568
krytyczny		.		krytycz				# 269
krytyk			.		krytyk				# 2153
kryzys			.		kryzys				# 580
krzyk			.		krzy(k|cz)			# 4328
kukla			.		kuk[łl]				# 53
kurator			k		\bkurato			# 29
kurde			.		kurd[eę]			# 2093
kustykac		.		(?<!a)ku[śs]ty			# 19
kwiczec			.		kwi(k|cz)			# 195
lachy			.		\b[łl]ach			#
lament			.		\blament			# 224
lekkomyslny		u		lekkomy				# 5
len			u		\ble(ń|ni)\w*				# TODO 1912 lenin
lgac			.		\b[ł](ga|[żz]e)\w*		# 109
libacja			.		libac[jk]\w+			# 38
loch			.		\bloch(\b|u|[óo]w|em|ami)		# TODO lochy (swinie)
mafia			k		\bmafi				# 1498
malwersacje		k		malwers				# 32
manowce			.		manowce				# 5
marnotrawny		.		marnotraw			# 80
marnowac		.		marnow				# 599
meczyc			.		m[ęe]cz(ony|[ąa]c)			# TODO 870 meczach męczy-meczy
miernota		.		miern\w*				# TODO
mizerny			f		mizern				# 3
monotonia		.		monoton(?!icz)			# 40
monstrualny		.		\bmonstru			# 18
motloch			.		mot[łl]och\w*			# 100
mroczny			.		\bmro(cz|k)			# 379
nagana			.		nagan(?!ia)			# 56
narazic			.		nara(zi\b|zi[ćcłl]|[żz][oa])	# 173
narkotyki		k		narko[tm]			# 337
nawiedzony		u		nawiedzo			# 39
nedza			.		n[ęe]dz				# 194
negatywne		.		ne(gatywn|gacja|gow)		# 395
nicosc			.		nico[śs][ćc]			# 19
nieaktywny		.		nieaktyw			# 70
niechlubny		.		niechlub			# 45
nieciekawy		.		nieciekaw			# 1044
niecny			.		niecn				# 9
nieczuly		.		nieczu[lł]			# 105
nieczysty		.		nieczy[śs][tc]			# 134
niedobrze		.		niedobr				# 628
niedoczekanie		.		niedoczek			# 58
niedopatrzenie		.		niedopat			# 13
niedopowiedzenie	.		niedopow		# 21
niedopuszczalny		.		niedopu				# 134
niedorzeczny		.		niedorzeczn\w+			# 45
niedoskonaly		.		niedoskon			# 45
niedoszly		.		niedosz				# 152
niedozwolony		k		niedozwol			# 22
niedozywiony		.		niedożyw			# 43
niedrozny		.		niedro(żz)			# 0
niedzialajacy		.		\bniedzia			# 22
niedzorzeczny		.		niedorze			# 45
niegodziwy		.		niegodziw			# 71
niekomfortowy		.		niekomfort			# 55
niekontrolowany		.		niekontrol			# 36
niekorzystny		.		niekorzy			# 297
nielaska		.		nie[łl]ask			# 10
nielegalny		.		nielegal			# 541
nielogiczny		.		nielogi				# 30
niemily			.		niemi[łl]			# 547
niemowa			.		\bniemow[^l]\w*			# 8
niemozliwy		.		niemo[żz]liw			# 1090
nienormalny		m		nienormal			# 147
nieobliczalny		.		nieoblicz			# 14
nieodpowiedni		.		nieodpowiedn			# 86
nieodpowiedzialny	.		nieodpowiedz			# 134
nieodwracalny		.		nieodwrac			# 67
nieoptymalny		.		(nie|sub)optym			# 1
niepewny		.		niepewn				# 124
nieplanowany		.		nieplan				# 5
niepokoj		.		niepok[óo][ji]			# 447
niepoprawny		.		niepopraw			# 91
nieporadny		.		nieporad			# 49
nieporozumienie		.		nieporoz			# 380
niepotrzebny		.		niepotrzeb			# 585
niepotwierdzony		.		niepotwier			# 65
niepowazny		.		niepowa				# 81
niepowodzenie		.		niepowodz			# 49
nieprawda		.		nieprawd			# 747
nieprawidlowy		.		nieprawi			# 478
nieprzewidywalny	.		nieprzewid			# 70
nieprzygotowany		.		nieprzyg			# 73
nieprzyjazny		.		nieprzyja			# 7
nieprzyjemny		.		nieprzyjem			# 95
nieprzyzwoity		.		nieprzyzw			# 43
nierealny		.		nierealn			# 245
nierozpoznany		.		nierozpoz			# 6
nieslusznie		.		nies[łl]usz			# 92
niesmialy		.		nie[śs]mia[łl]			# 181
niesmieszny		.		nie[śs]miesz			# 143
niesmieszny		.		nie[śs]miesz			# 143
niespawiedliwy		.		\bniespraw			# 296
niespojny		.		niesp[óo]j			# 6
niespokojny		.		niespoko			# 25
niesprawdzony		.		niesprawdz			# 11
niesprawny		.		niesprawn			# 30
niestabilny		.		niestabil			# 32
nieszczegolny		.		nieszczeg			# 6
nieszczery		.		nieszczer			# 53
nietakt			.		nietakt				# 8
nietolerancja		.		nietoler			# 36
nietrzezwy		.		nietrze[źz]			# 17
nietykalny		.		nietykal			# 71
nieuczciwy		k		nieuczc				# 48
nieudolny		.		nieudol				# 119
nieufny			.		nieufn				# 183
nieuprawniony		.		nieupraw			# 12
nieurodzaj		.		nieurodz			# 37
nieuzasadniony		.		nieuzasa			# 107
niewazny		.		niewa[żz]n			# 599
niewdzieczny		.		niewdzi				# 57
niewiele		.		niewiele			# 815
niewierny		.		niewiern			# 46
niewolnik		.		niewolni			# 166
niewybredny		.		niewybred			# 2
niewygodny		.		niewygod			# 232
niewygodny		.		niewygod			# 232
niewyjasniony		.		niewyja				# 104
niewykonalny		.		niewykonal			# 35
niewykorzystany		.		niewykorz			# 87
niewypal		.		niewypa[lł]			# 66
niewystarczajacy	.		niewystar			# 40
niezadowolony		.		niezadowol			# 150
niezdolny		.		niezdoln			# 319
niezgodny		.		niezgodn			# 193
nieznajomy		.		nieznajom			# 80
niezrozumialy		.		niezrozu			# 200
niezyciowy		.		nie[żz]yci			# 2
nijaki			.		nijak\w				# 92
niski			f		\bnisk\w+			# TODO 802 niskoemisyjny
nosz			.		\bnosz\b			# 153
nowobogactwo		.		nowobogac			# 9
nowomoda		.		nowomod				# 10
obalic			.		\bobali				# 73
obawa			s		\bobaw				# 1305
obelga			.		obel[gżz]\w*			# 99
obled			m		ob[łl][ęd]d			# 148
obwisly			f		obwi[śs]			# 5
oczerniac		k		oczern				# 95
odszkodowanie		k		odszkod				# 1016
odwolac			.		odwo[łl][aye]			# 1715
odwyk			.		odwyk				# 42
ograniczac		.		ogranicz			# 2550
okupowac		.		\bokup[oa]			# 884
opium			.		opium				# 51
opozniony		mu		(o|za)p[óo][źz]nion\w		# 75
ordynardny		.		ordynar\w*			# 154
ostrzezenie		.		\bostrze[gżz]			# 633
pacjent			m		pacjen				# 429
panika			.		pani(k|czn)			# 1183
paranoja		mu		paranoi				# 45
parobek			.		par[óo]b			# 26
parowka			.		par[óo]w				# TODO 230 parowy wyparowal
paszkwil		.		paszkw				# 45
pech			.		pe(ch\b|cha\b|ch[oe]\w|sz[yao])	# 456
pieprzyc		w		piepr\w+			# 3183
pipidowo		.		pipid				# 7
pisdu			.		pisd[auoy]\w*			# 224
placz			s		p[łl]a(cz|ka[^t])		# 10818
plagiat			k		plagia				# 94
pogarda			.		\b(pogard|wzgard|gardz)		# 1460
pokuta			.		pokut				# 64
pomowienie		k		pom[óo]wi			# 97
pomylic			.		pomyl[ioe]			# 525
pomylka			.		pomy[łl]k			# 214
popelnic		.		\bpope[łl]			# 1692
popiol			.		popi[óo][łl]			# 34
porazka			.		pora[zż][e]?k			# 1068
potepiac		.		pot[ęe]p			# 342
potknac			.		potkn				# 595
potwor			.		potw[óo]r			# 452 potwornie
pozar			.		po[żz]ar(\b|[^tlł])		# 503
pozegnac		.		po[żz]egna			# 728 żegnać
precz			.		precz				# 1033
problem			.		problem				# 11258
prochno			.		pr[óo]chn(?!ik)			# 22
profanowac		r		profan[aou]			# 81
prowizorka		.		prowizor			# 30
prozaiczne		.		prozaicz			# 16
przegapic		.		(prze|za|z)gapi[ćcłl]		# 216
przeginac		.		przegi				# 212
przeholowac		.		prze[c]?hol			# 1
przeklestwa		.		przekl([i]?n|[ęe][ńn])		# 553
przepasc		.		przepa[śs][ćc]			# 220
przerazenie		.		\bprzera[zż]			# 1333
przestepca		k		przest[ęe]p[^oni]		# 1732
przesyt			.		przesy[tc]			# 125
przeszkoda		.		przeszk[óoa]d			# 1939 przeszkoda
przymus			.		przymus				# 392
przypal			.		przypa[lł]			# 228
pseudo			.		\bpseudo(?!ni)			# 733
pudlo			.		[s]?pud[łl][ao]			# 610
pysk			f		pysk\w*				# 758 FP
ranic			.		(\b|z)rani[ćcłlo]		# 1058
ranny			.		\brann				# 157 FP
rdza			.		(\b|za|prze|od)rdz			# TODO 119 TODO rdzen rdzenny
redukcja		.		reduk				# 127
rezygnacja		.		rezygn				# 1058
rozdarty		.		rozdar				# 71
rozgardiasz		.		rozgardiasz			# 11
rozpadac		.		\brozpad			# 921
rozstroj		.		rozstr[oó]			# 0
rozwod			.		rozw[óo]d			# 113
ruina			.		ru[ij]n\w*			# 598 FP
ryczec			.		(?<!p)rycz[ęeaąy]		# 2312
ryj			f		\bryj\w*			# 3871
rynsztok		o		rynszto				# 64
sadlo			f		\bsad[łl][oae]\w*		# 20 sadlok
sarkazm			.		sarka[sm]			# 61
schizofrenia		mu		schiz				# 128
separacja		.		separ				# 32
sidla			.		(?<!roman)sid[e]?[łl]			# 22 TODO
skandal			.		skandal				# 2339
skarzyc			k		skar[żzg]			# 2610
skazany			.		\bskaza[ćcnń]			# 800
skazywac		.		\bskaz(a[łl]|uj|yw)		# 96
skleroza		mu		sklero[tz]			# 29
skostnialy		.		skostnia			# 9
skrajny			.		skrajn				# 389
skreslic		.		(s|prze)kre[śs]l		# 137
skrupuly		.		skrupu(?!la)			# 485
slaby			.		s[lł]ab\w+			# 5978
slepy			m		[śs]lep\w+			# 607
slumsy			.		\bsl[au]ms			# 15
spam			.		spam\w*				# 3074
spisek			.		spis[e]?k			# 628
sprawca			k		\bsprawc[^i]			# 333
sprzeciw		.		sprzeciw			# 333
sprzeczny		.		sprzecz				# 462
strach			.		stra(ch|sz)			# 7230
strata			.		\b(u|s)tra[tc]			# 7577
szatan			r		s[z]?atan			# 296
szkalowac		.		szkal				# 444
szkielet		ss		szkielet			# 33
szkody			.		\bszk[óo]d			# 7112
szmira			.		\bszmir				# 14
szok			.		szok				# 3038
szowinizm		.		szowini				# 118
sztuczny		.		sztuczn				# 353
tandeta			.		tandet\w+			# 53
tendencyjny		.		tendencyj			# 116
tlusty			f		t[łl]u[śs]			# 361
totalny			.		totaln				# 3351 totalnie
tragiczny		.		tragi[cz]			# 787
trauma			m		traum				# 258
trudno			.		\btrudn[oiay]			# 3151
tupet			.		\btupe[tc]			# 73
ublizac			.		ubli[żz]\w+			# 111
ujma			.		\bujm[ay]			# 8
ulom			u		u[łl]om\w+			# 97
upadac			.		\bupad				# 1480
uposledzony		m		upo[śs]led			# 127
uraz			.		\b(|po)uraz			# 227
urojenia		mu		\buro[ji]			# 151
utytlany		f		\w*tyt[łl]a\w*			# 2
wiezienie		k		wi[ęe]zie[nń]			# 1302
wkurzac			.		wkurz				# 1996
wpadka			.		wpadk				# 1042
wredny			.		wredn\w+			# 1283
wstyd			.		wstyd\w*			# 3176
wulgarny		.		wulgar				# 517
wyc			.		\b(za|roz|)wy([ćc]|je\w*|[łl](|y|i|i[śs]\w+))\b		# TODO wychowanie wychodzic wycofac wyciag wycieczka wyjechac
wyciek			.		\bwyciek			# 177
wykroczenie		k		wykrocz[^n]			# 47
wynaturzenie		.		wynaturz			# 1
wynocha			.		\bwyno(ch|ś\b|[śs]cie)		# 18
wypadek			.		wypad[e]?k			# 2556
wypraszac		.		wypr(asz|osz|osi)		# 57
wyrok			k		wyrok				# 1166
wyrzucic		.		wyrzuc				# 1264
wysmiewac		.		(wy|prze)[śs]miew		# 641
zagrozenie		.		\bzagro[żz]			# 2330
zakaz			.		zakaz				# 2797
zakladnik		.		zak[łl]adni			# 146
zalamac			.		za[łl]am[ak]			# 527
zalamac			.		za[łl]am\w+			# 752
zalosc			.		\b[żz]a[łl]o[sś]\w+		# 2101
zalosny			.		[żz]a[łl]o[sś][cćn]\w*		# 2219
zastoj			.		zast[óo]j			# 1
zatrzymac		.		zatrzym				# 5597
zawiesc			.		zaw(iod|ied|odz|ie[śs][ćc])	# 1385
zazdrosc		.		zazdro[sś][ncćz]		# 3270
zblazowany		.		zblazo				# 4
zdrada			.		zdra[dj]			# 3773
zebrac			.		żebra					# TODO 152 TODO żebra(MED)
zenujacy		.		za[żz]eno|żenu			# 1502
zgielk			.		zgie[łl]k			# 24
zgraja			.		\bzgraj[iao]			# 10
zgroza			.		zgroz				# 77
zgryzota		.		zgry(zo[tc]|[źz]l)			# 3 TODO zgryzota zgryzliwy rozgryzac
zlom			.		z[łl]om				# 162
zly			.		\b[źz][lł][eyoiaąu]\b		# 9488 zly zle zlo zlymi zla
znieslawic		k		nies[łl]aw			# 280 nieslawny
zombie			.		zombi				# 543
zostawic		.		\b(po|)zostaw			# 3898
zwiac			.		\b(z|na)wi[ae][ćcłl]		# 63
patologia		?		patol\w*			# 1573
rusek			?		\brus(ek|cy|ki|ka|ko)		# 2192
uzurpator		?		uzurp\w+			# 25
amok			am		\bamok(\b|u|iem)		# 159
anihilacja		a		anihil				# 12
armata			a		\barmat(?!or|ur)		# 118 -armatura -armator
bagnet			a		bagnet				# 379
bandyta			ak		\bbandy[ct]			# 528
banowac			a		\b(z|po|)ban(\b|y\b|ow)		# 868
bejsbol			a		bej[sz]bol			# 9
bojowka			a		boj[óo]w[e]?k			# 30
brutalny		a		brutaln				# 259
bunt			a		(\b|z)bunt			# 343
chuligan		a		chulig				# 47
deptac			a		\b(za|z|roz|po|)dep(t|cz)(?!ak)		# TODO 168 adept deptak
gnebic			a		gn[ęe]bi			# 88
gniew			a		gniew					# TODO 627 zbigniew
grabic			a		(za|roz)grab				# TODO 44 grabic?
gwalt			a		gwa[łl]t(?!own)			# 253
jatka			a		\bjatk[ai]			# 3
kaganiec		a		kaga(ni|[ńn]c)			# 121
kajdanki		ak		kajdan				# 379
kanibal			a		kanibal				# 21
karabin			a		karabin				# 55
kastrowac		a		kastr				# 42
katusze			a		katusz				# 42
klocic			a		k[łl][óo][tc](\b|[^k])		# 1296
konflikt		a		konflikt			# 634
kopnac			a		kopn\w+				# 481 kopac
kradl			ak		krad[łlzn]\w*			# 3313
lupic			a		\b(z|roz|)[łl]upi[cćł]		# 14
maczeta			a		maczet				# 18
masakra			a		masakr\w*			# 1035
masochista		a		masochi[sz]			# 72 sado maso
napad			a		napad				# 301
napasc			a		napa(st|[śs][ćc])		# 1010
nauczka			a		nauczk				# 103
niebezpieczny		a		niebezp				# 703
nienawisc		a		nienawi[dśs]			# 6168
niszczyc		a		niszcz\w*			# 3281
nozownik		a		no[żz]owni			# 6
oblawa			a		ob[łl]aw			# 41
odwet			a		odwet				# 108
ofiara			a		ofiar				# 3267
okrutny			a		okru[ct]			# 556
oprawca			a		oprawc				# 158
pacyfikowac		a		pacyfik[aou]\w			# 263
palowac			a		pa[łl]owa			# 97
pistolet		a		pistolet			# 58
podstep			a		podst[ęe]p			# 385
pokonac			a		pokon[ay]			# 628
postrzelic		a		postrz[ea][lł]			# 287
pregierz		a		pr[ęe]gierz			# 10
przeciwnik		a		przeciwni[kc]			# 451
przegrac		a		przegr[ay]			# 3737
przemoc			a		przemoc				# 939
pulapka			a		pu[łl]apk			# 107
pyskowac		a		pysk(at|[oó]w|uj)		# 60
rabowac			ak		rabowa\w+			# 88
rabunek			ak		rabun[e]?k\w*			# 105
rozdzierac		a		rozdzier			# 2424
rozjechac		a		rozjech				# 95
rozroba			a		rozr[aóo]b([^i]|\b)		# 20
sadysta			a		sady[sz]			# 41 sado maso
siekiera		a		siekier[^k]			# 88
spoliczkowac		a		spoliczko			# 3
starcie			a		star(cia|[ćc]\b)		# 103
szantaz			ak		szanta[żz]			# 189
szydzic			a		szydz\w+			# 213
szykany			a		szykan				# 288
terror			a		terror\w*			# 1010
tortury			a		tortur				# 292
truc			a		tru(ci[zce]|[łlt][ayoi])		# TODO 157 truly(ANG) trucizna vs truc
uderzenie		a		[uz]derz				# TODO 2903 zderzenie
unicestwic		a		unicest				# 23
ustawka			a		ustawk				# 2331
wbijac			a		wbi[ćcj]			# 652
wojna			a		(?<!pod)woj[e]?n		# 9524 -podwojnie
wojownik		a		woj[oó]w			# 251
wrogi			a		wr[óo]g				# 2535
wrzeczec		a		wrzeszcz			# 138
wsciekly		a		w[śs]ciek			# 482
wsciekly		a		w[śs]ciek\w+			# 481
wtargnac		a		\bwtarg				# 31
wybuch			a		wybuch				# 811
wyludzic		a		wy[łl]udz			# 1705
wyrwac			a		\bwyr[y]?w			# 1240
zadyma			a		\bzadym				# 257
zajumac			a		juma[ćclł]			# 27
zamach			a		zamach\w*			# 1995 zamachowski
zaminowac		a		\b(pod|za)minow[au]		# 0
zaognic			a		zaogni				# 5
zaorac			a		\b(za|prze|wy|roz|)ora[ćcłln]		# TODO 1093 orange
zatarg			a		\bzatarg			# 496
zboj			a		zb[óo]j\w*			# 130 zbojkotowac
zlamac			a		\b(|po|od|z|roz)łama		# 1891
zlosc			a		\bz[łl]o[śs]			# 693
zmusic			a		zmus[zi]			# 1066
znecac			a		\bzn[ęe]c\w			# 191
agresja			aa		agres[^t]			# 2180
atak			aa		(\b|za)atak			# 5108
awantura		aa		awantur\w*			# 543
bestialski		aa		bestial\w*			# 111
bojka			aa		b[óo]j(k(?!ot)|ek)		# 32
bomba			aa		bomb(?!el|oni)			# 1180
demolowac		aa		demol				# 140 demoludy
dewastowac		aa		dewast				# 78
egzekucja		aa		egzeku				# 118 egzekutywa
elektrowstrzasy		aa		elektrows			# 3
katowac			aa		\b(|s|za)katow(?!ic)		# 360
manipulacja		ap		manipul\w+			# 1094
pogrom			ass		pogrom				# 342
zastrzelic		ass		(za|roz|powy)strzel		# 203
szwab			d		szwab\w*			# 339
zydzic			dd		(?<![rs])[żz]ydzi[łlćc]		# 18
endek			h		ende[ck]\w*			# 62 czy moze byc obrazliwe?
esbek			h		\besbe\w*			# 80
faszyzm			h		faszy[sz]			# 751
folksdojcz		h		[fv]olksd			# 147
fuhrer			h		f[uü][h]?rer			# 87
gestapo			h		gestap				# 236
getto			h		\bg[h]?ett(|o|a|cie|ach|om)\b	# 97
gulag			h		gu[łl]ag\w*			# 49
hitler			h		hitler\w*			# 390
iluminaci		h		il[l]?umina			# 37
kolaborant		h		kolabor\w+			# 398
kolchoz			h		ko[łl][c]?hoz\z*		# 73
komuch			h		komu(ch|sz)				# TODO 
komunizm		h		komuni[sz]			# 1816
koncentracyjny		h		koncentracy			# 153
lenin			h		lenin\w*			# 237
lewak			h		lewa[ck]\w*			# 2851
lustrowac		h		\blustr(ow|ac)			# 11
lwp			h		\blwp				# 52
marks			h		marks\w*			# 934
masoneria		h		maso[nń]			# 181
milicja			h		\bmilic				# 97
nazizm			h		nazi\w*				# 1001
niekoszerny		h		niekoszer			# 23
nkwd			h		nkwd				# 494
pasiak			h		pasiak				# 28
pislam			h		pislam\w*			# 56
plebejusz		h		pleb[e]\w*			# 62-plebs
plebs			h		pleb[s]\w*			# 62-plebe
podczlowiek		h		pod(cz[łl]ow|lud)\w+		# 56
prl			h		peerel|\bprl			# 1345
sb			h		\bsb(\b|-)			# 7031 slang:siebie
sierp			h		sierp(\b|[^in])			# 51
socjalizm		h		socjali				# 607
ssman			h		\b[e]?s[e]?sman\w*		# 5
stalin			h		stalin\w*			# 459
swolocz			h		swo[łl]oc\w+			# 71
sybir			h		syb[ie]r			# 220
syjonista		h		syjo(nis|[ńn]sk)		# 174
szmalcownik		h		szmalcow\w+			# 116
targowica		h		targowic			# 294
ub			h		\bub(\b|-)			# 1003 uber ublizac
ubek			h		\bube[ck]\w*			# 241
zabor			h		zab[óo]r			# 67
zomo			h		\bzomo				# 398
zydo			h		\b[żz]yd(k|o[^wm])		# 1047
bolszewia		hh		bolszew\w*			# 791
holocaust		hs		holo[ck]a			# 989
alkoholik		im		alkoholik\w*			# 97
amator			i		amator				# 330
amoralny		i		amoraln				# 14
analfabeta		iu		analfab				# 82
arogancki		i		arogan				# 753
babsztyl		i		babszt\w+			# 52
balwan			i		ba[łl]wan			# 29
bankrut			ik		bankru[tc]			# 249
barachlo		i		barach[łl]			# 62
barbarzynca		i		barbarz					# TODO 161 barbarze
becwal			i		b[ęe]cwa			# 2
bekart			i		b[ęe]kar[tc]			# 22
bezmyslny		iu		bezmy[śs]ln			# 84
blazen			i		b[łl]a[zź][e]?n			# 147
brzydki			if		brzyd[kc]			# 3056
bufon			i		bufon				# 30
burak			i		bura\w+				# 397
cherlawy		if		herlaw				# 3
ciamajda		i		ciamajd				# 31
ciolek			i		\bcio[łl][e]?k			# 37
ciul			i		ciul\w*				# 193
cpun			i		\b[ćc]pun\w*			# 31
cwaniak			i		cwania				# 491
cwel			i		cwel\w*				# 131
cymbal			iu		cymba[łl]			# 216
cynik			i		\bcyni\w+			# 182
cynik			i		cyni(k|cz|zm)			# 181
debil			iu		debil\w*			# 3172
defetysta		i		defety[sz]			# 16
dluznik			ik		(?<!po)d[łl]u[żz]n[iy](\b|[kc])	# 16
donosiciel		ik		donosicie			# 177
dran			i		\bdra[ńn]			# 98
durny			i		dur(n\w+|e[ńn])				# TODO durny vs duren
dyletant		i		dyleta				# 9
dziad			i		dziad(|[^ek]|[^ek]\w+)\b		# 1244 TODO dziadek dziadkowie
egoista			i		egoi				# 105
fircyk			i		fircyk\w*			# 12
frajer			iu		frajer\w*			# 522
gach			i		\bgach\w*			# 45
gadula			i		\bgadu[lł]\w*			# 4
gbur			i		gbur\w+				# 5
glab			iu		\bg[łl][ąa]b			# 123
gluchy			i		g[łl]uch\w+			# 410
glupi			i		g[łl]up\w+			# 7826
hipokryta		i		hipokry\w+			# 668
hipster			i		hipster				# 241
hochsztapler		i		hochsztapl\w+			# 2211
idiota			iu		\bidio\w+			# 3147
ignorant		iu		ignoran[tc]\w*			# 293
imbecyl			imu		imbecy				# 44
jelen			iu		jele[ńn]\w*			# FP
jelop			iu		je[łl]op\w*			# 86
kapus			i		kapu[śs](\b|[iuó]\w*)		# 35
katol			ir		katol(\b|i\b|[ea]\w*)		# 152
kibol			i		kibo\w*				# 762
klakier			i		klakier				# 21
kmiot			i		\bkmi[eo]			# 100
koles			i		\bkole[śs]			# 1591
konus			if		konus\w*			# 946
kretacz			i		kr[ęe]tac\w+			# 103
kretyn			imu		\bkrety\w+			# 817
kuglarz			i		kuglar\w+			# 47
kulawy			im		\bkul(aw|ej)\w+			# 86
klamca			iu		kłam\w+				# 3499
lajdak			i		[lł]ajda\w+			# 45
lajza			i		[lł]ajz				# 116
luj			i		\bluj				# 72
lysy			if		\b[łl]ys\w+			# 359 wylysiec
malkontent		i		malkon				# 36
maniak			iu		maniak				# 107
matol			iu		mato[łl]			# 264
matol			iu		mato[łl]\w*			# 263
nachalny		i		nachaln\w*			# 32
naiwny			i		naiwn\w+			# 534
niedojda		i		niedojd				# 45
niedorajda		i		niedorajd			# 4
niedorozwiniety		imu		niedoroz			# 27
niedowartosciowany	i		niedowart			# 274
niekompetentny		i		niekompet			# 126
nierob			i		nier[óo]b			# 84
nieudacznik		i		\bnieudaczni\w+			# 203
nieudacznik		i		nieudacz			# 212
nieudacznik		i		nieudan				# 158
nieuk			i		nie(do|)u[kc]			# 264
niezrownowazony		i		niezr[óo]wno			# 30
nikczemny		i		nikcz				# 60
oblakany		imu		ob[łl][ąa]kan			# 40
oprych			i		opry(ch|szk)\w*			# 4
oszolom			i		oszo[łl]om\w*			# 146
oszust			ik		\boszu(st|k)\w*			# 2417
pajac			i		pajac\w*			# 919
palant			i		palant				# 22
paser			i		paser 				# 14
pasztet			if		paszte[tc]			# 81 kulinarne:pasztet
patalach		i		pata[łl]a			# 24
pazerny			i		pazern\w+			# 155
pener			i		(?<!o)pener			# 5
perfidny		i		perfid				# 153
persona			i		person(a|y|ie|om)\b		# 107
pionek			i		\bpion[e]?k			# 26
pirat			i		\b(anty|)pira[ct]		# 198
podzegacz		i		pod[żz]eg			# 19
podly			i		pod[łl][ay]\w+				# TODO 174 podlasie podlany podlacasz
pokurcz			if		pokurcz				# 42
polglowek		iu		p[óo][łl]g[łl][óo]		# 12
pomagier		i		pomagier			# 5
prostak			i		\bprosta\w+			# 388
prymityw		i		prymityw\w*			# 485
psychiatra		im		psychiatr				# TODO ???
psychiczny		imu		psychicz				# TODO ??? psycholog psychika
psychol			imu		psychol(?!og)				# TODO psycholog psychika
sierota			i		siero[tc]			# 412
skurczybyk		i		kurczyb				# 12
snob			i		snob				# 15
swir			imu		[śs]wir\w+			# 505
szelma			i		szelm				# 0
szmata			i		szma[ct]\w*			# 2139
szpetny			if		szpet				# 15
szuja			i		\bszuj\w*			# 78
tluk			i		\bt[łl]uk(?!li)			# 411
tlumok			i		t[łl]umok			# 20
troglodyta		i		troglod				# 9
troll			i		(?<!pa|on|en)tro[l]?l(?!ogi)	# 1838 -kontrola -patrol -controll -astrologia -centrolew
tuman			iu		\btuman				# 63
wampir			i		wampir				# 674
warchol			i		warcho\w+			# 46
wariat			imu		wari(a[ct]|owa)\w*		# 614
wariat			imu		wari(at|ow|uj)			# 628
wazniak			i		wa[żz]nia			# 211
wscibski		i		w[śs]cib			# 9
wypalony		iu		wypal(on|e[ńn])			# 18
wyrzutek		i		wyrzut[e]?k			# 6
zachlanny		iu		zach[łl]ann			# 59
zadluzony		i		zad[łl]u[żz]			# 140
zadufany		iu		zaduf				# 22
zamroczony		i		(za|po)mro(cz|k)		# 27
zamulac			i		z[a]?mul			# 488
zlamas			i		z[łl]amas\w+			# 21
zlodziej		ik		złodziej\w*			# 1920
zuchwaly		i		zuchwa				# 71
zul			if		żul\w*				# 167
zwyrodnialy		i		zwyro[ld]			# 599
dawn			idm		\bd[ao][łlw]n(a|em|ach|om|owi)\b	# TODO 1182 TODO dawny dawno dawni dawna
retard			idmu		retard\w*			# 40
bambus			idd		bambus\w*			# FP
ciapaty			idd		ciapat\w+			# 22
czarnuch		idd		czarnuch\w*			# 10
murzyn			idd		murzy[nń]\w*			# 323
zoltek			idd		[żz][óo]lt[e]?k\w*		# 1 FP
ponury			si		ponur				# 170
posepny			si		pos[ęe]p			# 16
bezduszny		ir		bezdusz				# 24
judasz			ir		judasz				# 93
apatia			s		\bapat				# 15
bezbronny		s		bezbron				# 55
bezradny		s		bezrad				# 84
bezsilny		s		bezsil				# 97
krzywda			s		\w*krzywd\w+			# 1297
niebyt			s		niebyt\w*			# 33
niefajny		s		niefajn				# 66
nieszczescie		s		nieszcz[ęe][śs]			# 606
niewesoly		s		nieweso[łl]			# 7
przygnebiony		s		przygn[ęe]b			# 52
przykrosc		s		przykro[śs][ćc]			# 52
przykry			s		przykr(y|ym|ych|ymi|o|e|ego)\b	# 2523
pustka			s		\bpustk				# 893
rozczarowac		s		rozczarow\w+			# 721
rozpacz			s		rozpacz\w*			# 607
samotny			s		samotn				# 648
smutek			s		smut\w+				# 7207
stagnacja		s		stagn				# 18
bagno			o		bag(ie)?n			# 725
biegunka		o		biegunk				# 14
blizna			o		blizn				# 386
brodawki		o		brodaw[e]?k			# 0
brud			o		brud(\b|[neo]\w*)		# 1041
brzydzic		o		brzyd[zl]			# 4366
cholera			om		choler				# 4123
czopek			o		czop[e]?k			# 39
dzuma			om		d[żz]um				# 81
ekskrementy		o		ekskremen			# 1
fekalia			o		fekal\w*			# 21
fetor			o		fetor				# 24
gnic			o		gni([ćc]|[łl]\w*)\b		# 96
gnoj			o		gn[oó]j\w+			# 488
kanalia			o		kanali\w*			# 288
kila			om		\bki[łl](a|e|ę|y|om)\b		# 83 FP
kloaka			o		kloa[ck]\w*			# 10
klozet			o		klozet\w*			# 6
kompost			o		kompost				# 7
kupa			o		\bkup(a|y|ą|om|ami|o|ach)\b	# 319 kupie(kupowac)
lewatywa		om		lewatyw				# 32
macki			o		mac(ka|ki|ek|kom|kami)\b	# 73
makabra			o		makabr				# 28
malaria			om		malari				# 2
maszkara		o		maszkar				# 4
mdlosci			o		md[łl]o[śs]			# 39
menel			of		menel				# 99
mocz			o		mocz(|u|em)\b			# 79
niesmak			o		niesma[ck]			# 117
niestrawnosc		o		niestrawn			# 142
niezdrowy		o		niezdrow			# 105
nowotwor		om		nowotw				# 204
oblesny			o		oble([sś]|ch)\w*		# 87 oblech
obskurny		o		obskur				# 5
ochyda			o		ochyd\w+			# 129
odpad*			o		odpad				# 980
odraza			o		\bodra[zż]			# 180
ohyda			o		o[c]?hyd\w+			# 163
okropny			o		okropn				# 2920
oslizgly		o		o[śs]liz[g]?[łl]y		# 27
padlina			o		padlin				# 36
parszywy		o		parszyw				# 86
pierdziec		o		pierd(\b|[^oae.*])		# 1788
pisuar			o		pisuar\w*			# 42
plaga			o		plag(?!ia)			# 117
plesn			o		ple[śs][nń]			# 36 pleśnierowicz
pluc			o		(\b|o|wy)plu[ćctwłlj]		# 887
plugawy			o		plugaw				# 27
pryszcz			o		pryszcz\w*			# 291
rakotworczy		om		rakotw				# 0
sciek			o		\b[śs]ciek(\b|[^a])		# 70
slina			o		(\b|za|po|ob|wy)[śs]li[nń]		# TODO 150
smieci			o		[śs]mie[cć](|[^h]|[^h]\w+)\b	# 853
smierdzi		o		[śs]mierd\w+			# 652
smietnik		o		[śs]mietni\w+			# 183
smrod			o		smr[óo]d\w*			# 201
srac			o		sra[^cłlłnmj]\w+			# TODO 1444 -> sra
stechly			o		(s|za)t[ęe]ch			# 11
strup			o		\bstrup				# 7
syfilis			om		syfili[sz]			# 6
szajs			o		szajs\w+			# 163
szambo			o		szamb\w+			# 1292
szczac			oww		\b(|wy|ze|za|o|po)szcz(a\b|a[^w]|yn)	# TODO 138 szczaw
szumowina		o		szumowin\w*			# 50
toksyczny		o		toksy				# 166
wirus			om		wirus				# 318
wrzod			om		wrz[ód]d			# 5
wstret			o		wstr[ęe]t			# 146
wstret			o		wstr[ęe]t\w*			# 146
wymiotowac		o		wymio[ct][^lł]			# 337
zaraza			o		zaraz[ayo]			# 168
zarazic			o		zara([źz][nl]|[żz][oa]|zi|zk)	# 180
zepsuty			o		(\b|ze|po)psu[ćcłlt]		# 1992
zepsuty			o		(\b|ze|po|na)psu[jćcłlt]	# 2817
cuchnie			oo		cuchn\w+			# 75
pasożyt			oz		paso[żz]y			# 96
aborcja			mp		aborc[jiy]			# 1043
biurokracja		p		biurokra[tc]			# 57
demonstracja		p		demonst				# 1029
dezerter		p		dezer[tc]			# 58
dezinformacja		p		dezinfo				# 185
dyktator		p		dyktat[ou]r\w*				# TODO 
dymisja			p		dymis				# 1106
embargo			p		embarg				# 21
figurant		p		figuran[tc]			# 28
indoktrynacja		p		indoktryn			# 32
kapitulacja		p		kapitul([^yea]\b|\w\w)		# 52 kapituła
karierowicz		p		karierowicz\w*			# 26
kasta			p		kast(?!et|r)			# 799
konszachty		p		konszach			# 3
korupcja		p		koru(mpo|pcj)			# 299
kurupcja		p		korupc\w+			# 203
lapowka			p		\b[łl]ap[óo]w\w*		# 241
lobby			p		lobb				# 594
nuklearny		p		nuklear				# 345
oponen			p		op+on+ent			# 15
populizm		p		populi[sz]			# 466
prokurator		p		prokurat			# 4768
propaganda		p		propagand\w*			# 2171
protest			p		prote[śs]			# 10381
prowokacja		p		prowok				# 831
pucz			p		pucz				# 172
radykal			p		radyka[łl]			# 332
rebelia			p		rebeli				# 50
roszczenia		p		\broszcz[ye]			# 1342
sabotowac		p		sabot				# 174
strajk			p		strajk\w*			# 371
szpieg			p		szpieg				# 206
totalitarny		p		totali				# 90
tyran			p		tyra[nń]				# 57 TODO tyranie tyraniu
weto			p		(\b|za|po)[wv]eto		# 641
zatuszowac		p		(\b|za)tuszowa			# 16
czystki			paa		\bczyst[e]?k			# 65
agentura		pp		\bagentur			# 466 agent=232=FP
antypolskie		pp		antypol				# 1152
antysemita		pp		antysemi			# 1090
aparatczyk		pp		aparatczyk\w*			# 36
bankster		pp		bankster\w*			# 74
bojkot			pp		bojkot\w*			# 513
cenzura			pp		cenz[uo]r			# 2339
belzebub		r		belzeb				# 24
czarownica		r		czarownic			# 96
demagog			r		demagog\w*			# 87
demon			r		demon(?![st])			# 223
diabel			r		\bdiab[e]?[łl]			# 859
egzorcyzmy		r		egzorcy				# 113
fanatyk			r		\bfanat				# 126
grzech			r		grze(ch|sz)			# 701
herezja			r		here[zt]			# 50
jedza			r		\bjędz				# 98
pieklo			r		(\b|[^u])piek(ie)?[łl]		# 682
sekta			r		\bsek(t(?!or)|ci)		# 239 -sektor -sekcja -insekt
swietokradztwo		r		[śs]wi[ęe]tokrad		# 15
cmentarz		ss		cmentar				# 414
denat			ss		\bdenat(?!u)			# 3
ekshumacja		ss		ekshum				# 336
eutanazja		ss		\beutan				# 326
grob			ss		gr[óo]b				# 871
katastrofa		ss		katastrof			# 1031
krew			ss		kr(ew\b|wi|waw)			# 3151
ludobojstwo		ss		ludob[óo]j			# 512
martwy			ss		martw(?!i[ećcłl])\w		# 1222
mogila			ss		mogi[łl]			# 29
morderca		ss		\bmorder			# 448
morderstwo		ss		mord(er|ow)			# 2256
nekrofil		ss		nekrofil			# 12
nekrolog		ss		nekrolog			# 11
niezywy			ss		nie[żz]yw			# 22
owdowiec		ss		owdowi				# 0
pogrzeb			ss		pogrzeb				# 1369
pogrzeb			ss		pogrzeb				# 1369 FP
poronic			ss		poroni				# 22 poronin
rzez			ss		\brze[źz](\b|n|i)		# 191
samobojca		ss		samob[óo]j			# 698
scierwo			ss		[śs]cierw\w*			# 454
scierwo			ss		[śs]cierw			# 458
smierc			ss		[śs]mier[ćct]			# 5727
szubienica		ss		szubien				# 256
truchlo			ss		truch[lł]			# 33
trumna			ss		trum(ie)?n			# 247
trup			ss		\btrup				# 335
umarly			ss		umar[łl]			# 1191
umierac			ss		umier				# 2536
zabic			ss		zabi[cćtj]			# 3917
zabojstwo		ss		zab[óo]j\w			# 423
zagazowac		ss		zagazo				# 11
zaglada			ss		zagład					# TODO 93 zagladalem
zaloba			ss		\b[żz]a[łl]ob			# 95
zbrodnia		ss		zbrodn				# 2220
zdychac			ss		(?<!w)zdych			# 272
zgon			ss		(\b|ze)zgon			# 118
zmarly			ss		zmar[łl]			# 628
zwloki			ss		zw[łl]ok(?![lłęe])		# 128
agonia			.		\bagoni				# 83
biurwa			ww		biurw\w*			# 2
dupa			ww		\w*dup\w*			# 8323 dupek,dupka->1
fiut			ww		fiut				# 702
gowno			ww o		g[oó]wn\w+			# 3761
chuj			www		(?<!ko|[lł]u)chuj(\w|\b)|\bch[*.][*.]	# 10932 -zakochujemy -podkochujesz -podsluchuje
cipa			ww		\bcip\w*			# 187
kurwa			www		(k[u]+|q)[r]+(w\w+|ew)		# 43737
kutas			www		kuta\w+				# 749
pierdolic		www		pierd([oae]l|[.*]+)		# 17151
pizda			www		pi[zź]d\w+			# 1446
zajebisty		ww		jebi[śs]			# 4889 ????????????????????????????????????
jebac			www aa		jeb([^i]|i[^śs]|\b)		# 18362
alfons			x		alfons				# 61
cycki			w xf		cyc(?![hl])			# 992
fujara			xf		fujar\w*			# 29
kochanek		x		kochan([e]?k|ic)		# 155
kuper			xf		\bkup[e]?r\w*			# 43
kuska			xf		\bku[śs][ck](?!us)\w		# 6
tylek			xf		ty[łl](ek|ka|ecz)\w*		# 1534
wazelina		x		wazelin				# 111
zboczenie		x		\bzbo(cz|ko)			# 173
zdzira			x		zdzir				# 11
ciota			xdd		\bciot\w+			# 290 ciotka ciotecz
pedal			xdd		peda[lł]			# 858
analny			xx		\banal(\b|n)			# 63
dymac			xx		dyma[ćclł]\w*			# 123
dziwka			w xx		dziw[e]?k			# 264
eunuch			xx		eunuch				# 6
gej			xx		\bgej([eóoia]|\b)		# 757
impotencja		xxm		impoten				# 39
jadra			xxmf		j[ąa]d(er|ra)			# 39
lachociag		xx		la(ch|sk)oci[ąa]g		# 12
lubiezny		xx		lubie[żz]n\w+			# 6
pederasta		xx		peder\w+			# 85
pedofil			xx		pedofil				# 334
penis			xxmf		penis\w*			# 107
perwers			xx		perwer\w*			# 163
picz			w xx		picz				# 197
pochwa			xxmf		pochw(a|y|om|[eę])\b		# 25
poligamia		xx		poligam				# 32
prostytucja		xx		prostytu			# 117
puszczalski		xx		puszczals\w+			# 7
rozwiazly		xx		rozwi[ąa]z[łl]\w+		# 11
sodomia			xx		sodom[ia]			# 16
srom			xxmf		srom\w*					# TODO 41
wagina			xxmf		wagin				# 17
zoofil			xx		zoofil				# 8
ameba			z		\bameb				# 106
glizda			z		glizd				# 10
gnid			z		gnid				# 180
gnida			z		gnid\w*				# 174
karaluch		z		karaluch			# 28
kleszcz			z		kleszcz				# 688
knur			z		knur\w*				# 32
kundel			z		kund[e]?l\w*			# 253
larwa			z		larw				# 28
leming			z		lem[m]?in\w+			# 706
leszcz			z		(?<!k)leszcz				# 276 TODO leszczyński
malpa			z		ma[łl]p				# 612
osiol			z		\b(osio[łl]|os[łl][aeo]m|o[sś][łl][ae](?!p|b))		# TODO 616 oślepnę osłonić osławić osłabic posła jarosław XD
padalec			z		padal[e]?c			# 209 padalecki
papuga			z		papug				# 63
pawian			z		pawian				# 3
pluskwa			z		pluskw\w*			# 14 FP
robactwo		z		(\b|za|z)roba(k|ct|cz)		# 252
robak			z		roba(k|cz)			# 258
sep			z		sęp				# 40 posępny zasępić
skunks			z		skunks				# 6
sucz			z		sucz[yoeęaą]?\b			# 27
suka			z		\bsuk(|i|ą|om|ami|in\w+)\b	# 308
swinia			z		[śs]wi[ńn]\w*			# 1808 -> swinoujscie
szczur			z		szczur\w*			# 2004 FP
szkodnik		z		szkodni				# 273
szympans		z		szympans			# 13
tchorz			z		tch[óo]rz\w*			# 1303
wieloryb		zf		wieloryb\w*			# 35
wol			z		\bw[oó]ł(|u|y|em|owi|owe|owa|ami)\b	# 39
wszy			z		wsz(on|aw|y\b)\w+		# 25
zmija			z		\b[żz]mij			# 143
baran			zz		baran\w*			# 388 FP
bydlo			zz		byd[łl]\w+			# 843
burza			.		\bburz				# 3984 -zaburzenia -oburzenie -zburzyc -wyburzyc -gownoburza
zaburzenia		.		zaburz				# 640
wyburzyc		.		(z|wy|roz)burz			# 160
oburzenie		.		\boburz				# 618
morda			f		(?<!za|wy|po)mord(?!er)		# 2551 -zamordowac -wymordowac -pomordowac -morderca
mordowac		ss		\b(za|wy|po|)mordow		# 1790
klamstwo		.		(?<!re)k[łl]am(?!k)		# 4591 -klamke -klamka
rzygac			o		(?<!p|t)rzyg(?!l[ąa]d|oto)	# 2855 -przygladac -przygotowac -rozstrzygnie
palic			.		(?<!na)pal(i[ćcłl]|on|[ąa]c)	# 3364 -napalony
napalony		xu		napal(?!m)			# 92
obrazac			.		(?<!wy|ze)obraż[aoe]		# 1681 -wyobrazac -przeobrazac
tepy			.		\bt[ęe]p[yaeioą]		# 820 -stepy -występy
ruchac			xx		(?<![uebd])rucha\w*		# 1390 -zawierucha -uruchamia -udobruchac -odruchami
porno			xx		(?<!od)porno			# 1256 -odpornosc
nudne			.		nud[naąz]			# 2525 !nudnosci
syf			o		syf(?!ik[ao]|on)		# 429 -syfon -klasyfikacja -intensyfikacja -klasyfikowal
chory			m		chor[zaeouy](?!o)		# 5898 -choreo -chorzow
spadac			.		\bspad(?!ochr)			# 2972 -spadochron
ostry			.		\b(za|wy|)ostr[z]?([aą]\b|am|y\b|y[młl]|[eę]\b|[eę][jm])	# 769 -ostrzeglem -siostry -ostroznie -ostrzega -strzelac
zapomniec		.		(?<!nie)zapomni[ae]		# 3004 -niezapomniany
siniak			?		(?<!ko)siniak			# 1763 -kosiniakowe
presja			a		(?<!de|ks|im)presj		# 583 -depresja -ekspresja -impresja
depresja		smu		depres				# 461
lesbijka		xx		\ble[sz]bi			# 422 -lesba
lesba			xxdd		\ble[sz]b(\b|[^i])		# TODO 49 ?lesbos
prawak			p		prawa[kc](?!h)			# 406 -oprawach -sprawach
kal			o		\bka([łl]|le|[lł]em|[łl]u)\b	# 154 -kałuża -kalendarz -kaleka -kalesony
menda			i		\bmend([ayoą]|\b)		# 255
cham			i		\b(|od|z)cham([^pb]|\b)		# 4093 -kocham -slucham -zdycham -oddycham -kicham -wlochami -champion -chameleon -ruchamy -dopycham -dmucham -posluchamy -chamberlain
szczuc			a		(?<!mie)szczu[ćcjlł]\w+		# 412 -mieszczuch
rozwalic		a		rozwa[lł]			# 1320
wywalic			?		\b(|po)wywa[łl](?!c)		# 1667 -wywalczyc -przygotowywal -zachowywal -przechowywal -podladowywal
walic			a		\bwal[ioaąn](?![zrj])		# 2181 -walizki -walory -walijski
zawalic			.		\bzawal(i\b|[ioe]\w)		# 287 -zawale
nawalic			.		\b(po|)nawal[ioea]		# 316
uwalic			a		\buwal(?!n)			# 112
zwalic			a		\bzwa[lł](?![nc])		# TODO 329 ?zwał
powalic			a		\bpowal(?!c)			# 320
walczyc			a		\b(|z|za|po|wy)wal(k|cz)	# TODO 11612 wywalczyc ???????????????????????????????????
grozic			a		(?<!nie)(za|po|)gr[óoa](zi|[źżz])	# TODO 6958 niezagrozone
powazny			.		(?<!u)powa[żz]n			# 3263 -upoważnić
zenujacy		.		\b(za|)[żz]en(u|ad|ow)		# 2633 -zenon -zenobia
anormalny		im		\banormal			# 9
_			o		odby(t|ci)\w*			# TODO 139 odbycia odbycie odbyty
kara			.		\bkar([aąy]\b|ze\b|z[ąa]|om|am(?!b))		# 1297 -karykato -karzel -karambol
karny			.		\bkarn(?!ac|e[tc]|is|aw)	# 1478 TODO -karnacja -karnet -karnister -karnawal
spasly			f		spa[śs](i|[łl])			# TODO 47
niezbyt			.		niezbyt				# 345
zbytnio			.		zbytn				# 733
zbyteczny		.		zbytecz				# 9
niespecjalny		.		niespec				# 16
nienajlepszy		.		nienajlep			# 7
:|			.		([:;][-]?[|])|(😐)		# 775 >:|
:/			.		([:;][-]?[\\/])			# 10832 >:/
:(			s		([:;][-]?[(\[c<])|(😞)		# 13040 >:(
niedostateczny		.		niedostat			# 6
wygnanie		.		wyg(na|an|on)			# 118
upokorzenie		s		upok[oa]rz			# 871
x			.		przesadn			# 63
nadmiar			.		nadmi[ea]r			# 133
x			.		zb[ęe]dn			# 256
prozny			.		\bpr[óo][żz]n			# 180
dziura			.		dziur				# 1477
x			.		\bnie mo(g|[żz]n)		# 11735
x			.		\bnie lub			# 4561
x			.		\bnie wytrz			# 999
x			.		\bnie doczek			# 89
x			.		\bnie dost			# 2065
x			.		\bnie obch			# 403
x			.		\bnie zrob			# 1437
x			.		\bnie odp			# 
x			.		podejrz(e[ńnw]|an)		# 1039
x			.		\bnie polec			# 293
sztampa			.		sztamp				# 4
megaloman		.		megaloman			# 39
mitoman			.		mitoman				# 39
x			.		\bwon\b				# 568 ANG:won
fuck			.		fuck				# 1235 mindfuck motherfucker
damn			.		damn				# 268
x			.		\bnie ma			# 36171
x			.		zabr[ao]n			# 932
"""
SORT = 0
KEY = 'x'
TAG = 'f'
SELECT = ''
TOKENIZE = 1

# ostrzal

# przy pomocy różnych żalków, trolli, pisowskiej telewizji usiłuje się skompromitować, ośmieszyć, zadeptać protestujących…

# dreczyc zbrodnia goj wściekły
# łby wina drzeć złudzenia kulfon ograniczony groza zgryzota tyrać ból cierpieć
# odebrać zabrać zmarł zczezł
# zmęczenie mdlićd targac
# paniusia panisko typ persona
# locha loszka wyrodny
# okropny naciagac trzoda błagam? kleska goguś przypa
# przewrót wywrotowy odwołać sztywniak karierow dziki zdziczaly
# wygnac
# EMOTKI !!!


#key = 'x'
kind = negative


pattern = {}
tags = {}

for line in kind.strip().split('\n'):
	rec = re.split('\t+',line.rstrip())
	tags[rec[0]] = rec[1]
	pattern[rec[0]] = re.sub('[(](?![?\]])','(?:',rec[2])

def get_patterns(tag='',n=99):
	if tag:
		selected = [w for w in pattern if tag in tags[w]]
	else:
		selected = pattern.keys()
	for words in grouper(selected,n):
		words = filter(bool,words)
		#yield [(p,pattern[p]) for p in grp if p]
		re_text = '('+')|('.join([pattern[w] for w in words])+')'
		re_compiled = re.compile(re_text,re.U)
		yield words,re_compiled,re_text

if __name__ == "__main__":
	from collections import defaultdict,Counter
	from pprint import pprint
	from time import time
	t0 = time()
	
	if SORT:
		lines = kind.strip().split('\n')
		if SORT==4:
			def k(x):
				comment = re.split('\t+',x)[3]
				m = re.findall('\d+',comment)
				return -int(m[0]) if m else 0
			lines.sort(key=k)
		else:

			lines.sort(key=lambda x:(re.split('\t+',x)[SORT-1],re.split('\t+',x)[0]))
		for line in lines:
			if SELECT and SELECT not in line: continue
			if TAG and TAG not in re.split('\t+',line)[1]: continue
			print(line.rstrip().encode('utf8'))
		exit()
	
	
	selected_patterns = list(get_patterns(TAG))
	#selected_patterns = list(get_patterns())

	if KEY:
		p = pattern[KEY]
		print(p.encode('utf8'),'\n')
		test_re = re.compile(p,re.U)
		#exit()
	
	tf = defaultdict(Counter)
	all = []
	#f = open(r'C:\repo\twitter\reference_7d.tsv')
	#f = open(r'C:\repo\war_room\data\reference_7d_v2.tsv')
	f = open(r'C:\repo\war_room\data\reference_7d.tsv')
	for i,line in enumerate(f):
		text = html.unescape(line.rstrip().split('\t')[-1].decode('utf8')).lower()
		text = tag_re.sub('#TAG',text)
		text = url_re.sub('#URL',text)
		text = usr_re.sub('#USER',text)
		if KEY:
			m = test_re.findall(text)
			if m:
				if TOKENIZE:
					for t in re.findall('(?u)\w+',text):
						if test_re.findall(t):
							tf[KEY][t] += 1
				print(text.encode('utf8'))
				all.extend(m)
		elif 0: # TF
			v = []
			tokens = re.findall('(?u)\w+',text)
			for words,compiled,_ in selected_patterns:
				for t in tokens:
					matches = compiled.findall(t)
					for m in matches:
						v.extend([(w,t) for w,x in zip(words,m) if x])
			for w,t in v:
				tf[w][t] += 1
			if 0 and v:
				print(len(v),v,text.encode('utf8'))
			if i%1000==1:
				print(i-1,1.0*i/(time()-t0),'/s')
			if i>=10000: break
		else:
			v = []
			for words,compiled,_ in selected_patterns:
				matches = compiled.findall(text)
				for m in matches:
					v.extend([w for w,t in zip(words,m) if t])
			if v:
				print(len(v),v,[tags[x] for x in v],text.encode('utf8'))	
	print('')
	if TOKENIZE:
		for t,f in tf[KEY].most_common(1000):
			print(KEY,len(tf[KEY]),t.encode('utf8'),f,sep='\t')
	if 1:
		print(len(all))
	if 0:
		fo = open('tf_nie_bez_top10k.tsv','w')
		for i,(k,v) in enumerate(tf.most_common(10000)):
			print(i+1,k.encode('utf8'),v,sep='\t',file=fo)
	if 0:
		fo = open('word_tokens.txt','wb')
		for w in sorted(tf):
			for t,f in tf[w].most_common(1000):
				print(w.encode('utf8'),len(tf[w]),t.encode('utf8'),f,sep='\t',file=fo)
	print(time()-t0) # 50s / tf=480s
