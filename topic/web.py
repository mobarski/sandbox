from bottle import route, run, template

from contrib import *
text = KO('data/text')
tokens = KO('data/tokens')
freq = KO('data/freq')
tf = KO('data/tf')
df = KO('data/df')
tfa = KO('data/tfa')
tfb = KO('data/tfb')

@route('/keys')
def get_keys():
	keys = text.keys()
	return ['{0} <a href="/text/{0}">text</a> <a href="/tokens/{0}">tokens</a> <a href="/freq/{0}">freq</a> <br>'.format(k) for k in keys]


@route('/text/<id>')
def get_text(id):
	return text[id]

@route('/tokens/<id>')
def get_tokens(id):
	return tokens[id]

@route('/freq/<id>')
def get_freq(id):
	out = []
	tf,before,after = freq[id]
	for t,f in desc(tf):
		b_str = u' '.join(u'{0} _ {1}'.format(tb,fb) for tb,fb in desc(before.get(t,{}),3,2))
		a_str = u' '.join(u'_ {0} {1}'.format(ta,fa) for ta,fa in desc(after.get(t,{}),3,2))
		out.append(u'{0} {1} {2} -- {3}'.format(t,f,a_str,b_str))
	return u'<br>'.join(out)

@route('/tf')
def get_tf():
	out = []
	for t,f in desc(tf):
		if f>=2:
			#a = u'<a href="/tfa/{0}">after</a>'.format(t)
			#b = u'<a href="/tfb/{0}">after</a>'.format(t)
			a=b=''
			out.append(u'{0} {1} {2} {3}'.format(t,f,b,a))
	return u'<br>'.join(out)

@route('/df')
def get_df():
	out = []
	for t,f in desc(df):
		if f>=2:
			#a = u'<a href="/tfa/{0}">after</a>'.format(t)
			#b = u'<a href="/tfb/{0}">after</a>'.format(t)
			a=b=''
			out.append(u'{0} {1} {2} {3}'.format(t,f,b,a))
	return u'<br>'.join(out)

@route(u'/tfa/<t>')
def get_tfa(t):
	out = []
	for t,f in desc(tfa[t.decode('utf8')]):
		if f>=2:
			out.append(u'_ {0} {1}'.format(t,f))
	return u'<br>'.join(out)


@route(u'/tfb/<t>')
def get_tfb(t):
	out = []
	for t,f in desc(tfb[t.decode('utf8')]):
		if f>=2:
			out.append(u'{0} _ {1}'.format(t,f))
	return u'<br>'.join(out)


def desc(d,limit=None,v_min=1):
	return [(k,v) for k,v in sorted(d.items(), key=lambda x:x[1],reverse=True) if v>=v_min][:limit]

run(host='localhost', port=9090)
