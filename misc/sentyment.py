# encoding: utf8

import re
from HTMLParser import HTMLParser
html = HTMLParser()

# TODO - re do odfiltrowania

url_re = re.compile(u'(?u)http[s]?://[\w/.-]+[\w]')
usr_re = re.compile(u'(?u)@\w+')
tag_re = re.compile(u'(?u)#\w+')

##test_re = re.compile(u'(?u)fajn\w+') # 11688

#test_re = re.compile(u'(?u)(ku|q)rw\w+') # 43737
#test_re = re.compile(u'(?u)chuj\w+') # 5077
#test_re = re.compile(u'(?u)pi[zź]d\w+') # 1446
#test_re = re.compile(u'(?u)jeba\w+') # 12359 -> jeb,zjeb,jebi itp
#test_re = re.compile(u'(?u)pierd\w+') # 19138
#test_re = re.compile(u'(?u)beznadz\w+') # 791
#test_re = re.compile(u'(?u)g[łl]up\w+') # 7826
#test_re = re.compile(u'(?u)szamb\w+') # 1292
#test_re = re.compile(u'(?u)komuch\w+') # 397
#test_re = re.compile(u'(?u)sra[^cłlłnmj]\w+') # 1444 -> sra
#test_re = re.compile(ur'(?u)\bcham[^p]\w+') # 2750
#test_re = re.compile(ur'(?u)\bprosta\w+') # 388
#test_re = re.compile(ur'(?u)\bnieudaczni\w+') # 203
#test_re = re.compile(ur'(?u)\bkrety\w+') # 817
#stest_re = re.compile(ur'(?u)\bidio\w+') # 3147
#test_re = re.compile(ur'(?u)durn\w+') # 1020
#test_re = re.compile(ur'(?u)bzdu\w+') # 962
#test_re = re.compile(ur'(?u)pod[łl][ay]\w+') # 174
#test_re = re.compile(ur'(?u)ochyd\w+') # 129
#test_re = re.compile(ur'(?u)kłam\w+') # 3499
#test_re = re.compile(ur'(?u)gn[oó]j\w+') # 488
#test_re = re.compile(ur'(?u)g[oó]wn\w+') # 3761
#test_re = re.compile(ur'(?u)szajs\w+') # 163
#test_re = re.compile(ur'(?u)piepr\w+') # 3183
#test_re = re.compile(ur'(?u)kuta\w+') # 749
#test_re = re.compile(ur'(?u)\bryj\w*') # 3871
#test_re = re.compile(ur'(?u)debil\w*') # 3172
#test_re = re.compile(ur'(?u)pajac\w*') # 919
#test_re = re.compile(ur'(?u)bura\w+') # 397
#test_re = re.compile(ur'(?u)frajer\w*') # 522
#test_re = re.compile(ur'(?u)szma[ct]\w*') # 2139
#test_re = re.compile(ur'(?u)[śs]wi[ńn]\w*') # 1808 -> swinoujscie
#test_re = re.compile(ur'(?u)mierno\w*') # 262
#test_re = re.compile(ur'(?u)bolszew\w*') # 791
#test_re = re.compile(ur'(?u)łajda\w+') # 41
#test_re = re.compile(ur'(?u)peda[lł]') # 858
#test_re = re.compile(ur'(?u)peder\w+') # 85
#test_re = re.compile(ur'(?u)\bciot\w+') # 290 ciotka ciotecz
#test_re = re.compile(ur'(?u)\b[żz]a[łl]o[sś]\w+') # 2101
#test_re = re.compile(ur'(?u)rucha\w*') # 1572
#test_re = re.compile(ur'(?u)rzyg\w*') # 9158 przygladac przygotowac
#test_re = re.compile(ur'(?u)lewa[ck]\w*') # 2851
#test_re = re.compile(ur'(?u)prawak\w*') # 235
#test_re = re.compile(ur'(?u)brzyd\w*') # 7237
#test_re = re.compile(ur'(?u)[śs]mierd\w+') # 652
#test_re = re.compile(ur'(?u)oble[sś]\w*') # 87 oblech
#test_re = re.compile(ur'(?u)murzy[nń]\w*') # 323
#test_re = re.compile(ur'(?u)sucz\b') # 25
#test_re = re.compile(ur'(?u)gbur\w+') # 5
#test_re = re.compile(ur'(?u)wredn\w+') # 1283
#test_re = re.compile(ur'(?u)iryt\w+') # 1733
#test_re = re.compile(ur'(?u)(?<!re)k[łl]am\w*') # 4625 klamke klamka
#test_re = re.compile(ur'(?u)krad[łlzn]\w*') # 3313
#test_re = re.compile(ur'(?u)złodziej\w*') # 1920
#test_re = re.compile(ur'(?u)patol\w*') # 1573
#test_re = re.compile(ur'(?u)konus\w*') # 946
#test_re = re.compile(ur'(?u)\bdno\w*') # 703
#test_re = re.compile(ur'(?u)[śs]cierw\w*') # 454
#test_re = re.compile(ur'(?u)gorsz\w+') # 9542
#test_re = re.compile(u'(?u)s[lł]ab\w+') # 5978
#test_re = re.compile(u'(?u)psych\w+') # 3951 psycholog psychika
#test_re = re.compile(u'(?u)szczu[ćcjlł]\w+') # mieszczuch?
#test_re = re.compile(u'(?u)elyt\w*') # 65
#test_re = re.compile(u'(?u)pleb[se]\w*') # 62
#test_re = re.compile(u'(?u)bzdur\w+') # 808
#test_re = re.compile(u'(?u)[lł]ajda\w+') # 45
#test_re = re.compile(u'(?u)badziew\w*') # 94
#test_re = re.compile(u'(?u)[żz]a[łl]o[sś][cćn]\w*') # 2219
#test_re = re.compile(u'(?u)gimb\w+') # 280
#test_re = re.compile(u'(?u)rozczarow\w+') # 721
#test_re = re.compile(u'(?u)niedorzeczn\w+') # 45
#test_re = re.compile(u'(?u)za[łl]am\w+') # 752
#test_re = re.compile(ur'(?u)\bcip\w*') # 187
#test_re = re.compile(u'(?u)gnid\w*') # 174
#test_re = re.compile(ur'(?u)\bszuj\w*') # 78
#test_re = re.compile(ur'(?u)dyma[ćclł]\w*') # 123
test_re = re.compile(ur'(?u)kibo\w*') # 762

# paszczur suka lemming troll beton groteskowe wydymali gach spadaj kundle zawszone gołodupiec naiwny motłoch
#test_re = re.compile(u'(?u)[żz]art\w*') # 7547 mozart

i = 0 
f = open('reference_7d.tsv')
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
