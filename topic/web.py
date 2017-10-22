from bottle import route, run, template

from contrib import *
text = KV('data/text.db',5)
tokens = KV('data/tokens.db',5)
freq = KV('data/freq.db',5)

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
		b_str = u' '.join(u'{0} {1}'.format(tb,fb) for tb,fb in desc(before.get(t,{}),3,2))
		a_str = u' '.join(u'{0} {1}'.format(ta,fa) for ta,fa in desc(after.get(t,{}),3,2))
		out.append(u'{0} {1} {2} -- {3}'.format(t,f,a_str,b_str))
	return u'<br>'.join(out)

def desc(d,limit=None,v_min=1):
	return [(k,v) for k,v in sorted(d.items(), key=lambda x:x[1],reverse=True) if v>=v_min][:limit]

run(host='localhost', port=9090)
