from bottle import route, run, template

from contrib import *
kv = KV('data/urlid_text.db',5,tab=1)

@route('/keys')
def keys():
    keys = kv.keys()
    return ['<a href="/text/{0}">{0}</a><br>'.format(k) for k in keys]


@route('/text/<id>')
def text(id):
    return kv[id]

run(host='localhost', port=9090)
