from flask import Flask, request
import ujson as json

kv = {}

app = Flask(__name__)

@app.route('/kv')
def kv_op():
	req = request
	op = req.args.get('op')
	if op=='get':
		k = req.args.get('k')
		v = json.dumps(kv.get(k))
		return v
	elif op=='set':
		k = req.args.get('k')
		v = req.args.get('v')
		kv[k] = v
		return json.dumps({'k':k,'v':v})

if __name__=="__main__":
	app.run(port=8080)
