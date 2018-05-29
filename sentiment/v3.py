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
# [s]mierc -> [n]nekro
# [a]gresja/przemoc
# se[x]ualnosc
# [o]dchody/[o]draza/nieczystosci/rozklad/zepsucie/choroby/brud
# [i]nwektywa
# [d]yskryminacja
# [w]ulgarne
#
# smute[k]
# [r]eligia
# bol, cierpienie, strach
# wymiar sprawiedliwosci / kodeks karny / prawo

# klucz  wulgarnosc  grupa  nietolerancja  wzorzec  notatki
negative = ur"""	
_			.		\bk(|u|ur)([*]+|[.][.]+)([aęeiy]|w[aęeiy])	# 206 k*rwa
aberracja		.		\baberr				# 14
aborcja			p		aborc[jiy]			# 1043
absurd			.		absurd				# 1635
absurd			.		absurd\w+			# 1410
agentura		pp		\bagentur			# 466 agent=232=FP
agonia			ss		\bagoni				# 83
agresja			aa		agres[^t]			# 2180
alfons			x		alfons				# 61
alienacja		.		alien(ow|ac)			# 4
alimenty		.		alimen				# 53
alkoholik		i		alkoholik\w*			# 97
amator			i		amator				# 330
amoralny		i		amoraln				# 14
analfabeta		i		analfab				# 82
anihilacja		a		anihil				# 12
anormalny		i		\banormal			# 
antypolskie		pp		antypol				# 1152
antysemita		pp		antysemi			# 1090
aparatczyk		pp		aparatczyk\w*			# 36
apatia			k		\bapat				# 15
areszt			.		\b(za|)areszt			# 1865
arogancki		i		arogan				# 753
atak			aa		(\b|za)atak			# 5108
atrapa			.		\batrap				# 105
awantura		aa		awantur\w*			# 543
awaria			.		\bawar[jiy]			# 234
babsztyl		i		babszt\w+			# 52
bac			.		\bbo(j[ęe]|imy)				# TODO 4240 bałem
badziew			.		badziew\w*			# 94
bagno			o		bag(ie)?n			# 725
bajzel			.		bajz[e]?l\w*			# 38
balagan			.		ba[łl]agan\w*			# 766
balast			.		balast				# 17
balwan			i		ba[łl]wan			# 29
bambus			idd		bambus\w*			# FP
banda			.		\bband(a|y|dzie)\b		# 510
bandyta			a		\bbandy[ct]			# 528
bankrut			i		bankru[tc]			# 249
bankster		pp		bankster\w*			# 74
barachlo		i		barach[łl]			# 62
baran			zz		baran\w*			# 388 FP
barbarzynca		i		barbarz				# 161
bat			.		\bbat(|a|em|u|y)\b		# 207
bazgroly		.		bazgr[oa]			# 39
becki			.		b[ęc]c[e]?k[i]?			# 12
becwal			i		b[ęe]cwa			# 2
bekart			i		b[ęe]kar[tc]			# 22
belkot			.		be[łl]ko[tc]			# 291
bestialski		aa		bestial\w*			# 111
besztac			.		beszt				# 5
bezbronny		k		bezbron				# 55
bezcelowy		.		bezcel				# 6
bezczelny		.		bezczel				# 605
bezczescic		.		bezcze[śs]			# 31
bezczynny		.		bezczyn				# 239
bezdenny		.		bezd[e]?n			# 16
bezdomny		.		bezdom				# 125
bezduszny		ir		bezdusz				# 24
bezkarny		.		bezkar				# 357
bezmiar			.		bezmiar				# 44
bezmozg			.		bezm[óo]zg\w*			# 75
bezmyslny		i		bezmy[śs]ln			# 84
beznadzieja		.		beznadz\w+			# 791
bezprawie		.		bezpraw				# 368
bezradny		k		bezrad				# 84
bezrobotny		.		bezrobo				# 181
bezsensowny		.		bezsens				# 379
bezsilny		k		bezsil				# 97
beztalencie		.		beztalen			# 12
bezwartosciowy		.		bezwarto			# 110
biadolic		.		\bbiado				# 60
bieda			.		bied[ayno]			# 2881
bierny			.		biern				# 472
biurokracja		p		biurokra[tc]			# 57
biurwa			w		biurw\w*			# 2
blad			.		\bbł[ąę]d			# 2467
blad			.		b[łl][ąaęe]d			# błędnik
blazen			i		b[łl]a[zź][e]?n			# 147
blizna			o		blizn				# 386
bluzgac			.		bluzg				# 78
bojka			aa		b[óo]j(k(?!ot)|ek)		# 32
bojkot			pp		bojkot\w*			# 513
bolszewia		hh		bolszew\w*			# 791
bomba			aa		bomb(?!el|oni)			# 1180
brak			.		brak				# 9193
brednie			.		\bbred[zn]			# 632
brodawki		o		brodaw[e]?k			# 0
brud			o		brud(\b|[neo]\w*)		# 1041
brutalny		a		brutaln				# 259
bufon			i		bufon				# 30
bunt			a		(\b|z)bunt			# 343
burak			i		bura\w+				# 397
burda			.		burd([ayę]|\b)			# 50
burza			.		burz				# 5491
bydlo			zz		byd[łl]\w+			# 843
bylejak			.		bylejak				# 23
bzdura			.		bzdu\w+				# 962
bzdury			.		bzdur\w+			# 808
cebula			.		cebul				# 345
cenzura			pp		cenz[uo]r			# 2339
chala			.		\bcha[łl]a			# 41
cham			i		\bcham([^p]|\b)				# TODO 
chaos			.		chao[st]			# 310
cherlawy		i		herlaw				# 3
chlac			.		\w*hlej|hla[cć]\w*		# 103
cholera			o		choler				# 4123
chory			.		chor[zaeouy]\w*			# 6087 choreo
chrzanic		.		chrzani				# 317
chuj			ww		chuj(\w|\b)|\bch[*.][*.]	# 11307 chujek->2
chuligan		a		chulig				# 47
chwast			.		hwast				# 58
ciamajda		i		ciamajd				# 31
ciapaty			idd		ciapat\w+			# 22
cierpiec		.		cierpi				# 1410
ciolek			i		\bcio[łl][e]?k			# 37
ciota			xdd		\bciot\w+			# 290 ciotka ciotecz
cipa			ww		\bcip\w*			# 187
ciul			i		ciul\w*				# 193
cmentarz		s		cmentar				# 414
cpun			i		\b[ćc]pun\w*			# 31
cuchnie			oo		cuchn\w+			# 75
cwaniak			i		cwania				# 491
cwel			i		cwel\w*				# 131
cycki			x		cyc(?![hl])			# 992
cymbal			i		cymba[łl]			# 216
cynik			i		\bcyni\w+			# 182
cynik			i		cyni(k|cz|zm)			# 181
czarnuch		idd		czarnuch\w*			# 10
czopek			o		czop[e]?k			# 39
czyhac			.		czyha				# 15
czystki			paa		\bczyst[e]?k			# 65
daremny			.		daremn				# 40
dawn			id		\bd[ao][łlw]n(a|em|ach|om|owi)\b	# 1182 TODO dawny dawno dawni dawna
debil			i		debil\w*			# 3172
defetysta		i		defety[sz]			# 16
deficyt			.		deficyt				# 100
degeneracja		.		degener\w+			# 646
dekiel			.		dek(iel|lem|la|lu|le)\b		# 96
demagog			r		demagog\w*			# 87
demaskowac		.		demask\w+			# 155
demolowac		aa		demol				# 140 demoludy
demotywowac		.		demotyw				# 2425
denerwowac		.		denerw				# 2513
dewastowac		aa		dewast				# 78
dezerter		p		dezer[tc]			# 58
dezinformacja		p		dezinfo				# 185
diabel			r		\bdiab[e]?[łl]			# 859
dluznik			i		(?<!po)d[łl]u[żz]n[iy](\b|[kc])	# 16
dno			.		\bdno\w*			# 703
dokuczac		.		dokucz				# 145
donos			.		donos\w*				# 1038 FP
donosiciel		i		donosicie			# 177
dopalacz		.		dopalacz			# 162
dramat			.		dramat				# 1127
dran			i		\bdra[ńn]			# 98
draznic			.		dra[żz]n			# 107
dreczyc			.		\b[u]?dr[ęe]cz			# 79
dupa			w		\w*dup\w*			# 8323 dupek,dupka->1 
durny			i		dur(n\w+|e[ńn])				# durny vs duren
dusic			.		(\b|u|przy|pod|za)du(si|sz[aąeęo])	# 1962 FP dusza
duszno			.		\bduszn				# 187
dyktator		p		dyktat[ou]r\w*			# 
dyletant		i		dyleta				# 9
dymac			xx		dyma[ćclł]\w*			# 123
dyskomfort		.		(nie|dys)komfort		# 75
dziad			i		dziad(|[^ek]|[^ek]\w+)\b	# 1244 dziadek dziadkowie
dziwka			xx		dziw[e]?k			# 264
dzuma			o		d[żz]um				# 81
egoista			i		egoi				# 105
egzekucja		aa		egzeku				# 118 egzekutywa
ekshumacja		s		ekshum				# 336
elektrowstrzasy		aa		elektrows			# 3
elyta			.		elyt\w*				# 65
embargo			p		embarg				# 21
endek			h		ende[ck]\w*			# 62 czy moze byc obrazliwe?
esbek			h		\besbe\w*			# 80
eunuch			xx		eunuch				# 6
eutanazja		s		\beutan				# 326
facjata			.		facja\w+			# 24
falsz			.		fa[łl]sz			# 2893
fanatyk			r		\bfanat				# 126
faszyzm			h		faszy[sz]			# 751
fatalny			.		fataln				# 445
fejk			.		fejk\w*				# 1178
fekalia			o		fekal\w*			# 21
fetor			o		fetor				# 24
figurant		p		figuran[tc]			# 28
fikcja			.		fikc[y]?j			# 1514
fircyk			i		fircyk\w*			# 12
fiut			w		fiut				# 702
flak			.		fla(k(?![oer])|cz)		# 69
folksdojcz		h		[fv]olksd			# 147
fortel			.		fortel				# 3
frajer			i		frajer\w*			# 522
fuhrer			h		f[uü][h]?rer			# 87
fujara			x		fujar\w*			# 29
gach			i		\bgach\w*			# 45
gadula			i		\bgadu[lł]\w*			# 4
garb			.		garb\w+				# 111 garbarnia
gbur			i		gbur\w+				# 5
geba			.		g[ęe]b[eayio]\w*		# 467 spongebob
gej			xx		\bgej([eóoia]|\b)		# 757
gestapo			h		gestap				# 236
getto			h		\bg[h]?ett(|o|a|cie|ach|om)\b	# 97
gimby			.		gimb\w+				# 280
glab			i		\bg[łl][ąa]b			# 123
glizda			z		glizd				# 10
gluchy			i		g[łl]uch\w+			# 410
glupi			i		g[łl]up\w+			# 7826
gnebic			a		gn[ęe]bi			# 88
gnic			o		gni([ćc]|[łl]\w*)\b		# 96
gnid			z		gnid				# 180
gnida			z		gnid\w*				# 174
gniew			a		gniew				# 627
gniot			.		\bgnio[tc](?![lł])		# 366
gniot			.		gniot\w*			# 452
gnoj			o		gn[oó]j\w+			# 488
gorszy			.		gorsz\w+			# 9542
gorzki			.		gorzk				# 288
gowno			wo		g[oó]wn\w+			# 3761
grabic			a		(za|roz)grab				# TODO 44 grabic?
granda			.		\bgrand(a|y)\b			# 14
grob			s		gr[óo]b				# 871
groteska		.		grotesk\w+			# 96
grozic			a		gr[óo](zi|[źżz])		# 
gruby			.		grub\w+				# 1435
gruchot			.		gruchot				# 8
gulag			h		gu[łl]ag\w*			# 49
gwalt			a		gwa[łl]t(?!own)			# 253
halas			.		\bha[łl]a[sś]			# 99
hanba			.		ha[ńn]b\w*			# 624
haniebny		.		hanieb				# 264
hazard			.		hazard				# 108
hejt			.		hejt				# 2844
herezja			r		here[zt]			# 50
hipokryta		i		hipokry\w+			# 668
hipster			i		hipster				# 241
histeria		.		hister				# 190
hitler			h		hitler\w*			# 390
hochsztapler		i		hochsztapl\w+			# 2211
holocaust		hs		holo[ck]a			# 989
holota			.		ho[łl]o[tc]			# 1521
horda			.		\bhord				# 35
horror			.		horror				# 247
hucpa			.		hucp				# 437
idiota			i		\bidio\w+			# 3147
ignorant		i		ignoran[tc]\w*			# 293
imbecyl			i		imbecy				# 44
impotencja		xx		impoten				# 39
incydent		.		incydent			# 56
indoktrynacja		p		indoktryn			# 32
infantylny		.		infantyl			# 24
intryga			.		intryg(?!uj|ow)			# 68
inwektywa		.		inwektyw			# 40
ironia			.		ironi				# 428
irytuje			.		iryt\w+				# 1733
jadra			xx		j[ąa]d(er|ra)			# 39
jadrowy			.		j[ąa]drow			# 94
jaja			.		\bjaj				# 3302
japa			.		\bjap[aąeęyi](\b|[^n]|[^n]\w+)		# TODO japonia japierdole
jatka			a		\bjatk[ai]			# 3
jelen			i		jele[ńn]\w*			# FP
jelop			i		je[łl]op\w*			# 86
jeniec			.		\bje([ńn]c|nie)\w		# 61
judasz			ir		judasz				# 93
judzic			.		judz[ia][ćc]			# 14
kablowac		.		(?<!o)kabl(uj|owa[ćcłl])	# 13
kaftan			.		kaftan(?!ik)			# 48
kaganiec		a		kaga(ni|[ńn]c)			# 121
kajdanki		a		kajdan				# 379
kal			o		\bka([ł]|le)\w*				# TODO kałuża
kanalia			o		kanali\w*			# 288
kanibal			a		kanibal				# 21
kantowac		.		kan(ciar|tow|tuj)			# 20 TODO krytykant
kapitulacja		p		kapitul([^yea]\b|\w\w)		# 52 kapituła
kapus			i		kapu[śs](\b|[iuó]\w*)		# 35
karalny			.		karaln				# 205
karaluch		z		karaluch			# 28
karierowicz		p		karierowicz\w*			# 26
kasta			p		kast(?!et|r)			# 799
kastrowac		a		kastr				# 42
katastrofa		s		katastrof			# 1031
katol			i		katol(\b|i\b|[ea]\w*)		# 152
katorga			.		\bkator[gżz]			# 24 lokatorzy
katowac			aa		\b(|s|za)katow(?!ic)		# 360
katusze			a		katusz				# 42
kibol			i		kibo\w*				# 762
kicz			.		\bkicz				# 68
kiepski			.		kiepsk				# 373
kila			o		\bki[łl](a|e|ę|y|om)\b		# 83 FP
klaki			.		\bk[łl]ak(?!ier)		# 54
klakier			i		klakier				# 21
klamca			i		(?<!re)k[łl]am\w*		# 4625 klamke klamka
klamot			.		klamot				# 0
klapa			.		klap[aynlłi]			# 142
kleska			.		\bkl[ęe]sk			# 245
kleszcz			z		kleszcz				# 688
klnac			.		\bkln				# 53
kloaka			o		kloa[ck]\w*			# 10
klocic			a		k[łl][óo][tc](\b|[^k])		# 1296
klozet			o		klozet\w*			# 6
kmiot			i		\bkmi[eo]			# 100
knebel			.		kneb(el|lo|li)			# 26
knur			z		knur\w*				# 32
kochanek		x		kochan([e]?k|ic)		# 155
kolaborant		h		kolabor\w+			# 398
kolchoz			h		ko[łl][c]?hoz\z*		# 73
koles			i		\bkole[śs]			# 1591
komornik		.		komornik			# 165
komplikacje		.		komplik				# 293
kompost			o		kompost				# 7
kompromitacja		.		kompromit			# 1206
komuch			h		komu(ch|sz)				#
komunizm		h		komuni[sz]			# 1816
koncentracyjny		h		koncentracy			# 153
kondolencje		.		kondolenc			# 22 FP
konflikt		a		konflikt			# 634
konszachty		p		konszach			# 3
konus			i		konus\w*			# 946
kopnac			a		kopn\w+				# 481 kopac
korupcja		p		koru(mpo|pcj)			# 299
koryto			.		kory[tc](a\b|o|i)		# 364
koszmar			.		koszmar				# 549
kpic			.		\bkpi				# 302
kradl			a		krad[łlzn]\w*			# 3313
kretacz			i		kr[ęe]tac\w+			# 103
kretyn			i		\bkrety\w+			# 817
krew			s		kr(ew\b|wi|waw)			# 3151
kryminal		.		krymina[łl]			# 3568
krytyczny		.		krytycz				# 269
krytyk			.		krytyk				# 2153
kryzys			.		kryzys				# 580
krzyk			.		krzy(k|cz)			# 4328
krzywda			k		\w*krzywd\w+			# 1297
kuglarz			i		kuglar\w+			# 47
kukla			.		kuk[łl]				# 53
kulawy			i		\bkul(aw|ej)\w+			# 86
kundel			z		kund[e]?l\w*			# 253
kupa			o		\bkup(a|y|ą|om|ami|o|ach)\b	# 319 kupie(kupowac)
kuper			x		\bkup[e]?r\w*			# 43
kurator			.		\bkurato			# 29
kurde			.		kurd[eę]			# 2093
kurupcja		p		korupc\w+			# 203
kurwa			ww		(k[u]+|q)[r]+(w\w+|ew)		# 43737
kustykac		.		(?<!a)ku[śs]ty			# 19
kutas			ww		kuta\w+				# 749
kwiczec			.		kwi(k|cz)			# 195
kłamca			i		kłam\w+				# 3499
lachociag		xx		la(ch|sk)oci[ąa]g		# 12
lachy			.		\b[łl]ach			# 
lajdak			i		[lł]ajda\w+			# 45
lajza			i		[lł]ajz				# 116
lament			.		\blament			# 224
lapowka			p		\b[łl]ap[óo]w\w*		# 241
larwa			z		larw				# 28
lekkomyslny		.		lekkomy				# 5
leming			z		lem[m]?in\w+			# 706
len			.		\ble(ń|ni)\w*			# 1912 lenin
lenin			h		lenin\w*			# 237
lesbijka		xx		\ble[sz]bi			# 422-lesba
lesba			xxdd		\ble[sz]b(\b|[^i])		# 
leszcz			z		(?<!k)leszcz			# 276 TODO leszczyński
lewak			h		lewa[ck]\w*			# 2851
lewatywa		o		lewatyw				# 32
lgac			.		\b[ł](ga|[żz]e)\w*		# 109
libacja			.		libac[jk]\w+			# 38
lobby			p		lobb				# 594
loch			.		\bloch(\b|u|[óo]w|em|ami)		# TODO lochy (swinie)
lubiezny		xx		lubie[żz]n\w+			# 6
ludobojstwo		s		ludob[óo]j			# 512
lupic			a		\b(z|roz|)[łl]upi[cćł]		# 14
lustrowac		h		\blustr(ow|ac)			# 11
lwp			h		\blwp				# 52
lysy			i		\b[łl]ys\w+			# 359 wylysiec
macki			o		mac(ka|ki|ek|kom|kami)\b	# 73
maczeta			a		maczet				# 18
mafia			.		\bmafi				# 1498
makabra			o		makabr				# 28
malaria			o		malari				# 2
malkontent		i		malkon				# 36
malpa			z		ma[łl]p				# 612
malwersacje		.		malwers				# 32
maniak			i		maniak				# 107
manipulacja		ap		manipul\w+			# 1094
manowce			.		manowce				# 5
marks			h		marks\w*			# 934
marnowac		.		marnow				# 599
marnotrawny		.		marnotraw			# 80
martwy			s		martw(?!i[ećcłl])\w		# 1222
masakra			a		masakr\w*			# 1035
masochista		a		masochi[sz]			# 72 sado maso
maszkara		o		maszkar				# 4
matol			i		mato[łl]			# 264
matol			i		mato[łl]\w*			# 263
mdlosci			o		md[łl]o[śs]			# 39
meczyc			.		m[ęe]cz(ony|[ąa]c)			# TODO 870 meczach męczy-meczy
menda			i		\bmenda\w*				# TODO
menel			o		menel				# 99
miernota		.		miern\w*			# 
milicja			h		\bmilic				# 97
mizerny			.		mizern				# 3
mocz			o		mocz(|u|em)\b			# 79
mogila			s		mogi[łl]			# 29
monotonia		.		monoton(?!icz)			# 40
monstrualny		.		\bmonstru			# 18
morda			.		mord(?!er)				# TODO >5000 morda
morderca		s		\bmorder			# 448
morderstwo		s		mord(er|ow)			# 2256
mordowac		s		\b(za|)mordow			# 1630
motloch			.		mot[łl]och\w*			# 100
mroczny			.		\bmro(cz|k)			# 379
murzynski		idd		murzy[nń]\w*			# 323
nachalny		i		nachaln\w*			# 32
nadmiar			.		nadmiar				# 73
nagana			.		nagan(?!ia)			# 56
naiwny			i		naiwn\w+			# 534
napad			a		napad				# 301
narazic			.		nara(zi\b|zi[ćcłl]|[żz][oa])	# 173
narkotyki		.		narko[tm]			# 337
nauczka			a		nauczk				# 103
nawiedzony		.		nawiedzo			# 39
nazizm			h		nazi\w*				# 1001
nedza			.		n[ęe]dz				# 194
negatywne		.		ne(gatywn|gacja|gow)		# 395
nekrofil		s		nekrofil			# 12
nekrolog		s		nekrolog			# 11
nicosc			.		nico[śs][ćc]			# 19
nieaktywny		.		nieaktyw			# 70
niebezpieczny		a		niebezp				# 703
niebyt			k		niebyt\w*			# 33
niechlubny		.		niechlub			# 45
nieciekawy		.		nieciekaw			# 1044
niecny			.		niecn				# 9
nieczuly		.		nieczu[lł]			# 105
nieczysty		.		nieczy[śs][tc]			# 134
niedobrze		.		niedobr				# 628
niedoczekanie		.		niedoczek			# 58
niedojda		i		niedojd				# 45
niedopatrzenie		.		niedopat			# 13
niedopowiedzenie	.		niedopow		# 21
niedopuszczalny		.		niedopu				# 134
niedorajda		i		niedorajd			# 4
niedorozwiniety		i		niedoroz			# 27
niedorzeczny		.		niedorzeczn\w+			# 45
niedoskonaly		.		niedoskon			# 45
niedoszly		.		niedosz				# 152
niedowartosciowany	i		niedowart			# 274
niedozwolony		.		niedozwol			# 22
niedozywiony		.		niedożyw			# 43
niedrozny		.		niedro(żz)			# 0
niedzialajacy		.		\bniedzia			# 22
niedzorzeczny		.		niedorze			# 45
niefajny		k		niefajn				# 66
niegodziwy		.		niegodziw			# 71
niekomfortowy		.		niekomfort			# 55
niekompetentny		i		niekompet			# 126
niekontrolowany		.		niekontrol			# 36
niekorzystny		.		niekorzy			# 297
nielaska		.		nie[łl]ask			# 10
nielegalny		.		nielegal			# 541
nielogiczny		.		nielogi				# 30
niemily			.		niemi[łl]			# 547
niemowa			.		\bniemow[^l]\w*			# 8
niemozliwy		.		niemo[żz]liw			# 1090
nienawisc		a		nienawi[dśs]			# 6168
nienormalny		.		nienormal			# 147
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
nierob			i		nier[óo]b			# 84
nierozpoznany		.		nierozpoz			# 6
nieslusznie		.		nies[łl]usz			# 92
niesmak			o		niesma[ck]			# 117
niesmialy		.		nie[śs]mia[łl]			# 181
niesmieszny		.		nie[śs]miesz			# 143
niesmieszny		.		nie[śs]miesz			# 143
niespawiedliwy		.		\bniespraw			# 296
niespojny		.		niesp[óo]j			# 6
niespokojny		.		niespoko			# 25
niesprawdzony		.		niesprawdz			# 11
niesprawny		.		niesprawn			# 30
niestabilny		.		niestabil			# 32
niestrawnosc		o		niestrawn			# 142
nieszczegolny		.		nieszczeg			# 6
nieszczery		.		nieszczer			# 53
nieszczescie		k		nieszcz[ęe][śs]			# 606
nietakt			.		nietakt				# 8
nietolerancja		.		nietoler			# 36
nietrzezwy		.		nietrze[źz]			# 17
nietykalny		.		nietykal			# 71
nieuczciwy		.		nieuczc				# 48
nieudacznik		i		\bnieudaczni\w+			# 203
nieudacznik		i		nieudacz			# 212
nieudacznik		i		nieudan				# 158
nieudolny		.		nieudol				# 119
nieufny			.		nieufn				# 183
nieuk			i		nie(do|)u[kc]			# 264
nieuprawniony		.		nieupraw			# 12
nieurodzaj		.		nieurodz			# 37
nieuzasadniony		.		nieuzasa			# 107
niewazny		.		niewa[żz]n			# 599
niewdzieczny		.		niewdzi				# 57
niewesoly		k		nieweso[łl]			# 7
niewiele		.		niewiele			# 815
niewierny		.		niewiern			# 46
niewolnik		.		niewolni			# 166
niewybredny		.		niewybred			# 2
niewygodny		.		niewygod			# 232
niewyjasniony		.		niewyja				# 104
niewykonalny		.		niewykonal			# 35
niewypal		.		niewypa[lł]			# 66
niewystarczajacy	.		niewystar			# 40
niezadowolony		.		niezadowol			# 150
niezdolny		.		niezdoln			# 319
niezdrowy		o		niezdrow			# 105
niezgodny		.		niezgodn			# 193
nieznajomy		.		nieznajom			# 80
niezrownowazony		i		niezr[óo]wno			# 30
niezrozumialy		.		niezrozu			# 200
niezyciowy		.		nie[żz]yci			# 2
niezywy			s		nie[żz]yw			# 22
nijaki			.		nijak\w				# 92
nikczemny		i		nikcz				# 60
niski			.		\bnisk\w+			# 802 niskoemisyjny
niszczyc		a		niszcz\w*			# 3281
niewykorzystany		.		niewykorz			# 87
niewygodny		.		niewygod			# 232
nkwd			h		nkwd				# 494
nosz			.		\bnosz\b			# 153
nowobogactwo		.		nowobogac			# 9
nowomoda		.		nowomod				# 10
nowotwor		o		nowotw				# 204
nuklearny		p		nuklear				# 345
obalic			.		\bobali				# 73
obawa			.		\bobaw				# 1305
obelga			.		obel[gżz]\w*			# 99
oblakany		i		ob[łl][ąa]kan			# 40
oblawa			a		ob[łl]aw			# 41
obled			.		ob[łl][ęd]d			# 148
oblesny			o		oble([sś]|ch)\w*		# 87 oblech
obrazac			.		obraż[aoe]			# 2886
obskurny		o		obskur				# 5
obwisly			.		obwi[śs]			# 5
ochyda			o		ochyd\w+			# 129
oczerniac		.		oczern				# 95
odbyt			o		odby(t|ci)\w*			# 139 odbycia
odpad*			o		odpad				# 980
odraza			o		\bodra[zż]			# 180
odszkodowanie		.		odszkod				# 1016
odwet			a		odwet				# 108
odwolac			.		odwo[łl][aye]			# 1715
odwyk			.		odwyk				# 42
ofiara			a		ofiar				# 3267
ograniczac		.		ogranicz			# 2550
ohyda			o		o[c]?hyd\w+			# 163
okropny			o		okropn				# 2920
okrutny			a		okru[ct]			# 556
okupowac		.		\bokup[oa]			# 884
opium			.		opium				# 51
oponen			p		op+on+ent			# 15
opozniony		.		(o|za)p[óo][źz]nion\w		# 75
oprawca			a		oprawc				# 158
oprych			i		opry(ch|szk)\w*			# 4
ordynardny		.		ordynar\w*			# 154
oslizgly		o		o[śs]liz[g]?[łl]y		# 27
ostry			.		ostr[yoe]\b			# 2122
ostrzezenie		.		\bostrze[gżz]			# 633
oszolom			i		oszo[łl]om\w*			# 146
oszust			i		\boszu(st|k)\w*			# 2417
owdowiec		s		owdowi				# 0
pacjent			.		pacjen				# 429
pacyfikowac		a		pacyfik[aou]\w			# 263
padalec			z		padal[e]?c			# 209 padalecki
padlina			o		padlin				# 36
pajac			i		pajac\w*			# 919
palant			i		palant				# 22
palic			.		pal(i[ćcłl]|on|[ąa]c)		# 3437
panika			.		pani(k|czn)			# 1183
papuga			z		papug				# 63
paranoja		.		paranoi				# 45
parobek			.		par[óo]b			# 26
parowka			.		par[óo]w			# 230
parszywy		o		parszyw				# 86
paser			i		paser 				# 14
pasiak			h		pasiak				# 28
pasożyt			oz		paso[żz]y			# 96
paszkwil		.		paszkw				# 45
pasztet			i		paszte[tc]			# 81 kulinarne:pasztet
patalach		i		pata[łl]a			# 24
patologia		?		patol\w*			# 1573
pawian			z		pawian				# 3
pazerny			i		pazern\w+			# 155
pedal			xdd		peda[lł]			# 858
pederasta		xx		peder\w+			# 85
pedofil			xx		pedofil				# 334
penis			xx		penis\w*			# 107
perfidny		i		perfid				# 153
persona			i		person(a|y|ie|om)\b		# 107
perwers			xx		perwer\w*			# 163
picz			xx		picz				# 197
pieklo			r		(\b|[^u])piek(ie)?[łl]		# 682
pieprzyc		.		piepr\w+			# 3183
pionek			i		\bpion[e]?k			# 26
pipidowo		.		pipid				# 7
pirat			i		\b(anty|)pira[ct]		# 198
pisdu			.		pisd[auoy]\w*			# 224
pislam			h		pislam\w*			# 56
pisuar			o		pisuar\w*			# 42
pizda			ww		pi[zź]d\w+			# 1446
placz			.		p[łl]a(cz|ka[^t])		# 10818
plaga			o		plag(?!ia)			# 117
plagiat			.		plagia				# 94
plebs			h		pleb[s]\w*			# 62-plebe
plebejusz		h		pleb[e]\w*			# 62-plebs
plesn			o		ple[śs][nń]			# 36 pleśnierowicz
pluc			o		(\b|o|wy)plu[ćctwłlj]		# 887
plugawy			o		plugaw				# 27
pluskwa			z		pluskw\w*			# 14 FP
pochwa			xx		pochw(a|y|om|[eę])\b		# 25
podczlowiek		h		pod(cz[łl]ow|lud)\w+		# 56
podstep			a		podst[ęe]p			# 385
podzegacz		i		pod[żz]eg			# 19
podły			i		pod[łl][ay]\w+			# 174
pogarda			.		\b(pogard|wzgard|gardz)		# 1460
pogrom			as		pogrom				# 342
pogrzeb			s		pogrzeb				# 1369
pogrzeb			s		pogrzeb				# 1369 FP
pokonac			a		pokon[ay]			# 628
pokurcz			i		pokurcz				# 42
pokuta			.		pokut				# 64
polglowek		i		p[óo][łl]g[łl][óo]		# 12
poligamia		xx		poligam				# 32
pomagier		i		pomagier			# 5
pomowienie		.		pom[óo]wi			# 97
pomylic			.		pomyl[ioe]			# 525
pomylka			.		pomy[łl]k			# 214
ponury			ik		ponur				# 170
popelnic		.		\bpope[łl]			# 1692
popiol			.		popi[óo][łl]			# 34
populizm		p		populi[sz]			# 466
porazka			.		pora[zż][e]?k			# 1068
poronic			s		poroni				# 22 poronin
posepny			ik		pos[ęe]p			# 16
potepiac		.		pot[ęe]p			# 342
potknac			.		potkn				# 595
potwor			.		potw[óo]r			# 452 potwornie
pozar			.		po[żz]ar(\b|[^tlł])		# 503
pozegnac		.		po[żz]egna			# 728 żegnać
prawak			p		prawa[kc]\w*			#
precz			.		precz				# 1033
pregierz		a		pr[ęe]gierz			# 10
presja			a		presj				# 975
prl			h		peerel|\bprl			# 1345
problem			.		problem				# 11258
prochno			.		pr[óo]chn(?!ik)			# 22
profanowac		.		profan[aou]			# 81
prokurator		p		prokurat			# 4768
propaganda		p		propagand\w*			# 2171
prostak			i		\bprosta\w+			# 388
prostytucja		xx		prostytu			# 117
protest			p		prote[śs]			# 10381
prowizorka		.		prowizor			# 30
prowokacja		p		prowok				# 831
prymityw		i		prymityw\w*			# 485
pryszcz			o		pryszcz\w*			# 291
przeciwnik		a		przeciwni[kc]			# 451
przegapic		.		(prze|za|z)gapi[ćcłl]		# 216
przeginac		.		przegi				# 212
przegrac		a		przegr[ay]			# 3737
przeholowac		.		prze[c]?hol			# 1
przeklestwa		.		przekl([i]?n|[ęe][ńn])		# 553
przemoc			a		przemoc				# 939
przepasc		.		przepa[śs][ćc]			# 220
przerazenie		.		\bprzera[zż]			# 1333
przestepca		.		przest[ęe]p[^oni]		# 1732
przeszkoda		.		przeszk[óoa]d			# 1939
przygnebiony		k		przygn[ęe]b			# 52
przykrosc		k		przykro[śs][ćc]			# 52
przykry			k		przykr(y|ym|ych|ymi|o|e|ego)\b	# 2523
przymus			.		przymus				# 392
przypal			.		przypa[lł]			# 228
pseudo			.		\bpseudo(?!ni)			# 733
psychol			i		psychol(?!og)			# psycholog psychika
psychiczny		i		psychicz				# ??? psycholog psychika
psychiatra		i		psychiatr				# ???
pucz			p		pucz				# 172
pudlo			.		[s]?pud[łl][ao]			# 610
pulapka			a		pu[łl]apk			# 107
pustka			k		\bpustk				# 893
puszczalski		xx		puszczals\w+			# 7
pysk			.		pysk\w*				# 758 FP	
pyskowac		a		pysk(at|[oó]w|uj)		# 60
rabowac			a		rabowa\w+			# 88
rabunek			a		rabun[e]?k\w*			# 105
radykal			p		radyka[łl]			# 332
rakotworczy		o		rakotw				# 0
ranic			.		(\b|z)rani[ćcłlo]		# 1058
ranny			.		\brann				# 157 FP
rdza			.		(\b|za|prze|od)rdz		# 119 TODO rdzen rdzenny
rebelia			p		rebeli				# 50
redukcja		.		reduk				# 127
retard			id		retard\w*			# 40
rezygnacja		.		rezygn				# 1058
robactwo		z		(\b|za|z)roba(k|ct|cz)		# 252
robak			z		roba(k|cz)			# 258
roszczenia		p		\broszcz[ye]			# 1342
rozczarowac		k		rozczarow\w+			# 721
rozdarty		.		rozdar				# 71
rozdzierac		a		rozdzier			# 2424
rozgardiasz		.		rozgardiasz			# 11
rozjechac		a		rozjech				# 95
rozpacz			k		rozpacz\w*			# 607
rozpadac		.		\brozpad			# 921
rozstroj		.		rozstr[oó]			# 0
rozwiazly		xx		rozwi[ąa]z[łl]\w+		# 11
rozwod			.		rozw[óo]d			# 113
ruchac			xx		rucha\w*			# 1572 zawierucha uruchamia
ruina			.		ru[ij]n\w*			# 598 FP
rusek			?		\brus(ek|cy|ki|ka|ko)		# 2192
ryczec			.		(?<!p)rycz[ęeaąy]		# 2312
ryj			.		\bryj\w*			# 3871
rzez			s		\brze[źz](\b|n|i)		# 191
sabotowac		p		sabot				# 174
sadlo			.		\bsad[łl][oae]\w*		# 20 sadlok
sadysta			a		sady[sz]			# 41 sado maso
samobojca		s		samob[óo]j			# 698
samotny			k		samotn				# 648
sarkazm			.		sarka[sm]			# 61
sb			h		\bsb(\b|-)			# 7031 slang:siebie
schizofrenia		.		schiz				# 128
sciek			o		\b[śs]ciek(\b|[^a])		# 70
scierwo			s		[śs]cierw\w*			# 454
sekta			r		\bsek(t(?!or)|ci)		# 239 sektor sekciarski sekcja insekt
sep			z		sęp				# 40 posępny zasępić
separacja		.		separ				# 32
sidla			.		(?<!roman)sid[e]?[łl]			# 22 TODO
sierota			i		siero[tc]			# 412
sierp			h		sierp(\b|[^in])			# 51
siniak			?		siniak				# 1923
skandal			.		skandal				# 2339
skarzyc			.		skar[żzg]			# 2610
skazany			.		\bskaza[ćcnń]			# 800
skazywac		.		\bskaz(a[łl]|uj|yw)		# 96
skleroza		.		sklero[tz]			# 29
skostnialy		.		skostnia			# 9
skrajny			.		skrajn				# 389
skreslic		.		(s|prze)kre[śs]l		# 137
skrupuly		.		skrupu(?!la)			# 485
skunks			z		skunks				# 6
skurczybyk		i		kurczyb				# 12
slaby			.		s[lł]ab\w+			# 5978
slepy			.		[śs]lep\w+			# 607
slina			o		(\b|za|po|ob|wy)[śs]li[nń]		# 150
slumsy			.		\bsl[au]ms			# 15
smieci			o		[śs]mie[cć](|[^h]|[^h]\w+)\b	# 853
smierc			s		[śs]mier[ćct]			# 5727
smierdzi		o		[śs]mierd\w+			# 652
smietnik		o		[śs]mietni\w+			# 183
smrod			o		smr[óo]d\w*			# 201
smutek			k		smut\w+				# 7207
snob			i		snob				# 15
socjalizm		h		socjali				# 607
sodomia			xx		sodom[ia]			# 16
spadac			.		\bspad				# 3099
spam			.		spam\w*				# 3074
spisek			.		spis[e]?k			# 628
spoliczkowac		a		spoliczko			# 3
sprawca			.		\bsprawc[^i]			# 333
sprzeciw		.		sprzeciw			# 333
sprzeczny		.		sprzecz				# 462
srac			o		sra[^cłlłnmj]\w+			# TODO 1444 -> sra
srom			xx		srom\w*					# TODO 41
ssman			h		\b[e]?s[e]?sman\w*		# 5
stagnacja		k		stagn				# 18
stalin			h		stalin\w*			# 459
starcie			a		star(cia|[ćc]\b)		# 103
stechly			o		(s|za)t[ęe]ch			# 11
strach			.		stra(ch|sz)			# 7230
strajk			p		strajk\w*			# 371
strata			.		\b(u|s)tra[tc]			# 7577
strup			o		\bstrup				# 7
sucz			z		sucz[yoeęaą]?\b			# 27
suka			z		\bsuk(|i|ą|om|ami|in\w+)\b	# 308
swietokradztwo		r		[śs]wi[ęe]tokrad		# 15
swinia			z		[śs]wi[ńn]\w*			# 1808 -> swinoujscie
swir			i		[śs]wir\w+			# 505
swolocz			h		swo[łl]oc\w+			# 71
sybir			h		syb[ie]r			# 220
syf			o		syf\w*					# 683 TODO syfon klasyfikacja intensyfikacja
syfilis			o		syfili[sz]			# 6
syjonista		h		syjo(nis|[ńn]sk)		# 174
szajs			o		szajs\w+			# 163
szambo			o		szamb\w+			# 1292
szantaz			a		szanta[żz]			# 189
szatan			.		s[z]?atan			# 296
szczac			o		\b(|wy|ze|za|o|po)szcz(a\b|a[^w]|yn)	# 138 szczaw
szczuc			a		szczu[ćcjlł]\w+			# mieszczuch?
szczur			z		szczur\w*			# 2004 FP
szelma			i		szelm				# 0
szkalowac		.		szkal				# 444
szkielet		.		szkielet			# 33
szkodnik		z		szkodni				# 273
szkody			.		\bszk[óo]d			# 7112
szmalcownik		h		szmalcow\w+			# 116
szmata			i		szma[ct]\w*			# 2139
szmira			.		\bszmir				# 14
szok			.		szok				# 3038
szowinizm		.		szowini				# 118
szpetny			i		szpet				# 15
szpieg			p		szpieg				# 206
sztuczny		.		sztuczn				# 353
szubienica		s		szubien				# 256
szuja			i		\bszuj\w*			# 78
szumowina		o		szumowin\w*			# 50
szwab			d		szwab\w*			# 339
szydzic			a		szydz\w+			# 213
szykany			a		szykan				# 288
szympans		z		szympans			# 13
tandeta			.		tandet\w+			# 53
targowica		h		targowic			# 294
tchorz			z		tch[óo]rz\w*			# 1303
tendencyjny		.		tendencyj			# 116
tepy			.		t[ęe]p[yaei]			# 2133
terror			a		terror\w*			# 1010
tluk			i		\bt[łl]uk(?!li)			# 411
tlumok			i		t[łl]umok			# 20
tlusty			.		t[łl]u[śs]			# 361
toksyczny		o		toksy				# 166
tortury			a		tortur				# 292
totalitarny		p		totali				# 90
totalny			.		totaln				# 3351 totalnie
tragiczny		.		tragi[cz]			# 787
trauma			.		traum				# 258
troglodyta		i		troglod				# 9
truc			a		tru(ci[zce]|[łlt][ayoi])		# TODO 157 truly(ANG) trucizna vs truc
truchlo			s		truch[lł]			# 33
trudno			.		\btrudn[oiay]			# 3151
trumna			s		trum(ie)?n			# 247
trup			s		\btrup				# 335
tuman			i		\btuman				# 63
tupet			.		\btupe[tc]			# 73
tylek			x		ty[łl](ek|ka|ecz)\w*		# 1534
tyran			p		tyra[nń]				# 57 TODO tyranie tyraniu
ub			h		\bub(\b|-)			# 1003 uber ublizac
ubek			h		\bube[ck]\w*			# 241
ublizac			.		ubli[żz]\w+			# 111
uderzenie		a		[uz]derz			# 2903
ujma			.		\bujm[ay]			# 8
ulom			.		u[łl]om\w+			# 97
umarly			s		umar[łl]			# 1191
umierac			s		umier				# 2536
unicestwic		a		unicest				# 23
upadac			.		\bupad				# 1480
upokorzenie		k		upokorz				# 584
uraz			.		\b(|po)uraz			# 227
urojenia		.		\buro[ji]			# 151
ustawka			a		ustawk				# 2331
utytlany		.		\w*tyt[łl]a\w*			# 2
uzurpator		?		uzurp\w+			# 25
wulgarny		.		wulgar				# 517
wampir			i		wampir				# 674
warchol			i		warcho\w+			# 46
wariat			i		wari(a[ct]|owa)\w*		# 614
wariat			i		wari(at|ow|uj)			# 628
wazelina		x		wazelin				# 111
wazniak			i		wa[żz]nia			# 211
weto			p		(\b|za|po)[wv]eto		# 641
wieloryb		z		wieloryb\w*			# 35
wiezienie		.		wi[ęe]zie[nń]			# 1302
wirus			o		wirus				# 318
wkurzac			.		wkurz				# 1996
wojna			a		woj[e]?n			# 9550
wojownik		a		woj[oó]w			# 251
wol			z		\bw[oó]ł(|u|y|em|owi|owe|owa|ami)\b	# 39
wpadka			.		wpadk				# 1042
wredny			.		wredn\w+			# 1283
wrogi			a		wr[óo]g				# 2535
wrzeczec		a		wrzeszcz			# 138
wrzod			o		wrz[ód]d			# 5
wscibski		i		w[śs]cib			# 9
wsciekly		a		w[śs]ciek			# 482
wsciekly		a		w[śs]ciek\w+			# 481
wstret			o		wstr[ęe]t			# 146
wstret			o		wstr[ęe]t\w*			# 146
wstyd			.		wstyd\w*			# 3176
wszy			z		wsz(on|aw|y\b)\w+		# 25
wtargnac		a		\bwtarg				# 31
wybuch			a		wybuch				# 811
wyc			.		\b(za|roz|)wy([ćc]|je\w*|[łl](|y|i|i[śs]\w+))\b		# TODO wychowanie wychodzic wycofac wyciag wycieczka
wyciek			.		\bwyciek			# 177
wykroczenie		.		wykrocz[^n]			# 47
wyludzic		a		wy[łl]udz			# 1705
wymiotowac		o		wymio[ct][^lł]			# 337
wynaturzenie		.		wynaturz			# 1
wynocha			.		\bwyno(ch|ś\b|[śs]cie)		# 18
wypadek			.		wypad[e]?k			# 2556
wypalony		i		wypal(on|e[ńn])			# 18
wypraszac		.		wypr(asz|osz|osi)		# 57
wyrok			.		wyrok				# 1166
wyrwac			a		\bwyr[y]?w			# 1240
wyrzutek		i		wyrzut[e]?k			# 6
wysmiewac		.		(wy|prze)[śs]miew		# 641
zabic			s		zabi[cćtj]			# 3917
zabojstwo		s		zab[óo]j\w			# 423
zabor			h		zab[óo]r			# 67
zachlanny		i		zach[łl]ann			# 59
zadluzony		i		zad[łl]u[żz]			# 140
zadufany		i		zaduf				# 22
zagazowac		s		zagazo				# 11
zaglada			s		zagład				# 93 zagladalem
zagrozenie		.		\bzagro[żz]			# 2330
zajumac			a		juma[ćclł]			# 27
zakaz			.		zakaz				# 2797
zakladnik		.		zak[łl]adni			# 146
zalamac			.		za[łl]am[ak]			# 527
zalamac			.		za[łl]am\w+			# 752
zaloba			s		\b[żz]a[łl]ob			# 95
zalosc			.		\b[żz]a[łl]o[sś]\w+		# 2101
zalosny			.		[żz]a[łl]o[sś][cćn]\w*		# 2219
zamach			a		zamach\w*			# 1995 zamachowski
zaminowac		a		\b(pod|za)minow[au]		# 0
zamroczony		i		(za|po)mro(cz|k)		# 27
zamulac			i		z[a]?mul			# 488
zaognic			a		zaogni				# 5
zaorac			a		\b(za|prze|wy|roz|)ora[ćcłln]	# 1093
zapomniec		.		zapomni[ae]			# 3087
zaraza			o		zaraz[ayo]			# 168
zarazic			o		zara([źz][nl]|[żz][oa]|zi|zk)	# 180
zastoj			.		zast[óo]j			# 1
zatarg			a		\bzatarg			# 496
zatrzymac		.		zatrzym				# 5597
zawiesc			.		zaw(iod|ied|odz|ie[śs][ćc])	# 1385
zazdrosc		.		zazdro[sś][ncćz]		# 3270
zblazowany		.		zblazo				# 4
zboczenie		x		\bzbo(cz|ko)			# 173
zboj			a		zb[óo]j\w*			# 130 zbojkotowac
zbrodnia		s		zbrodn				# 2220
zdrada			.		zdra[dj]			# 3773
zdychac			s		(?<!w)zdych			# 272
zdzira			x		zdzir				# 11
zebrac			.		żebra					# 152 TODO żebra(MED)
zenujacy		.		(za|\b)[żz]en(o|żenu|ad|ow|ua)	#
zenujacy		.		za[żz]eno|żenu			# 1502
zepsuty			o		(\b|ze|po)psu[ćcłlt]		# 1992
zepsuty			o		(\b|ze|po|na)psu[jćcłlt]	# 2817
zgielk			.		zgie[łl]k			# 24
zgon			s		(\b|ze)zgon			# 118
zgraja			.		\bzgraj[iao]			# 10
zgroza			.		zgroz				# 77
zgryzota		.		zgry(zo[tc]|[źz]l)		# 3 TODO zgryzota zgryzliwy rozgryzac
zlamac			a		\b(|po|od|z|roz)łama		# 1891
zlamas			i		z[łl]amas\w+			# 21
zlodziej		i		złodziej\w*			# 1920
zlom			.		z[łl]om				# 162
zlosc			a		\bz[łl]o[śs]			# 693
zmarly			s		zmar[łl]			# 628
zmija			z		\b[żz]mij			# 143
zmusic			a		zmus[zi]			# 1066
znecac			a		\bzn[ęe]c\w			# 191
znieslawic		.		nies[łl]aw			# 280 nieslawny
zoltek			idd		[żz][óo]lt[e]?k\w*		# 1 FP
zombie			.		zombi				# 543
zomo			h		\bzomo				# 398
zoofil			xx		zoofil				# 8
zostawic		.		\b(po|)zostaw			# 3898
zuchwaly		i		zuchwa				# 71
zul			i		żul\w*				# 167
zwalic			a		(?<!ro)zwa[lł]\w*			# TODO walic
rozwalic		a		rozwa[lł]				# TODO walic
zwiac			.		\b(z|na)wi[ae][ćcłl]		# 63
zwloki			s		zw[łl]ok(?![lłęe])		# 128
zwyrodnialy		i		zwyro[ld]			# 599
zydo			h		\b[żz]yd(k|o[^wm])		# 1047
niekoszerny		h		niekoszer			# 23
pierdziec		o		pierd(\b|[^oae.*])		# 1788
pierdolic		ww		pierd([oae]l|[.*]+)		# 17151
masoneria		h		maso[nń]			# 181
iluminaci		h		il[l]?umina			# 37
denat			s		\bdenat(?!u)			# 3
grzech			r		grze(ch|sz)			# 701
ekskrementy		o		ekskremen			# 1
ekstremalny		.		ekstrema			# 95
wagina			xx		wagin				# 17
analny			xx		\banal(\b|n)			# 63
porno			xx		porno				# 1312
kuska			x		\bku[śs][ck](?!us)\w		# 6
biegunka		o		biegunk				# 14
scierwo			s		[śs]cierw			# 458
pener			i		(?<!o)pener			# 5
luj			i		\bluj				# 72
bojowka			a		boj[óo]w[e]?k			# 30
palowac			a		pa[łl]owa			# 97
armata			a		\barmat(?!or)			#
zastrzelic		as		(za|roz|powy)strzel		# 203
postrzelic		a		postrz[ea][lł]			# 287
brzydki			i		brzyd[kc]			# 3056
brzydzic		o		brzyd[zl]			# 4366
dymisja			p		dymis				# 1106
eksmisja		.		\b(wy|)eksmi[st]		# 10
zadyma			a		\bzadym				# 257
rozroba			a		rozr[aóo]b([^i]|\b)		# 20
:(			k		([:;][-]?[(])|(😞)		# 11387 >:(
zajebisty		ww		jebi[śs]			# 4889 ????????????????????????????????????
rzygac			o		rzyg(?!l[ąa]d|oto)		# 4236 przygladac przygotowac
przesyt			.		przesy[tc]			# 125
zly			.		\b[źz][lł][eyoiaąu]\b		# 9488 zly zle zlo zlymi zla
jebac			wwaa		jeb([^i]|i[^śs]|\b)		# 18362
rynsztok		.		rynszto				# 64
ameba			z		\bameb				# 106
uposledzony		.		upo[śs]led			# 127
amok			a		\bamok(\b|u|iem)		# 159
pech			.		pe(ch\b|cha\b|ch[oe]\w|sz[yao])	# 456
troll			i		(?<!pa|on|en)tro[l]?l(?!ogi)	# 1838  kontrola patrol controll astrologia centrolew
prozaiczne		.		prozaicz			# 16
ciemnosc		.		ciemn				# 1499
deptac			a		\b(za|z|roz|po|)dep(t|cz)(?!ak)	# 168 adept deptak
zatuszowac		p		(\b|za)tuszowa			# 16
banowac			a		\b(z|po|)ban(\b|y\b|ow)		# 868
bac			.		\b(boj[ęe]|boisz|boi|boimy|boicie|boj[ąa]|b[óo]j|b[óo]jcie|ba[łl]em|ba[łl]am|ba[łl]o|bali[śs]my|ba[łl]y[śs]my|ba[łl]|ba[łl]a|ba[łl]o)\b		# 8402 TODO uproscic
bagnet			a		bagnet				# 379
wbijac			a		wbi[ćcj]			# 652
siekiera		a		siekier[^k]			# 88
bejsbol			a		bej[sz]bol			# 9
nozownik		a		no[żz]owni			# 6
pistolet		a		pistolet			# 58
karabin			a		karabin				# 55
napasc			a		napa(st|[śs][ćc])		# 1010
osiol			z		\b(osio[łl]|os[łl][aeo]m|o[sś][łl][ae](?!p|b))	# TODO 616 oślepnę osłonić osławić osłabic posła jarosław XD
zydzic			dd		(?<![rs])[żz]ydzi[łlćc]		# 18
wyrzucic		.		wyrzuc				# 1264
jedza			r		\bjędz				# 98
czarownica		r		czarownic			# 96
demon			r		demon(?![st])			# 223
demonstracja		p		demonst				# 1029
belzebub		r		belzeb				# 24
egzorcyzmy		r		egzorcy				# 113
"""
KEY = ''
TAG = 'a'
SORT = 2
# przy pomocy różnych żalków, trolli, pisowskiej telewizji usiłuje się skompromitować, ośmieszyć, zadeptać protestujących…

# dreczyc zbrodnia goj wściekły
# łby wina drzeć złudzenia kulfon ograniczony groza zgryzota tyrać ból cierpieć
# odebrać zabrać zmarł zczezł
# zmęczenie mdlićd targac
# paniusia panisko typ persona
# locha loszka wyrodny
# okropny naciagac trzoda błagam? kleska goguś przypa
# przewrót wywrotowy odwołać sztywniak karierow dziki zdziczaly
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
			print(line.rstrip().encode('utf8'))
		exit()
	
	selected_patterns = list(get_patterns(TAG))
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
				#v = [x for x in [filter(bool,x) for x in m] if x]
				print(text.encode('utf8'))
				all.extend(m)
		elif 1:
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
		else:
			v = []
			for words,compiled,_ in selected_patterns:
				matches = compiled.findall(text)
				for m in matches:
					v.extend([w for w,t in zip(words,m) if t])
			if v:
				print(len(v),v,[tags[x] for x in v],text.encode('utf8'))	
	print('')
	if 1:
		print(len(all))
	if 0:
		fo = open('tf_nie_bez_top10k.tsv','w')
		for i,(k,v) in enumerate(tf.most_common(10000)):
			print(i+1,k.encode('utf8'),v,sep='\t',file=fo)
	if 1:
		for w in sorted(tf):
			for t,f in tf[w].most_common(1000):
				print(w,len(tf[w]),t.encode('utf8'),f)
	print(time()-t0) # 50s / tf=480s
