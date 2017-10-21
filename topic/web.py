from bottle import route, run, template

from contrib import *
text = KV('data/text.db',5)
tokens = KV('data/tokens.db',5)

@route('/keys')
def get_keys():
    keys = text.keys()
    return ['{0} <a href="/text/{0}">text</a> <a href="/tokens/{0}">tokens</a><br>'.format(k) for k in keys]


@route('/text/<id>')
def get_text(id):
    return text[id]

@route('/tokens/<id>')
def get_tokens(id):
    return tokens[id]

run(host='localhost', port=9090)
