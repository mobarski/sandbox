from bottle import route,run,request
import ujson as json

kv = {}

@route('/kv')
def kv_op():
	req = request
	op = req.query.get('op')
	if op=='get':
		k = req.query.get('k')
		v = json.dumps(kv.get(k))
		return v
	elif op=='set':
		k = req.query.get('k')
		v = req.query.get('v')
		kv[k] = v
		return json.dumps({'k':k,'v':v})

#from gevent import monkey
#monkey.patch_all()
run(host='0.0.0.0',port=8080,server='meinheld')
