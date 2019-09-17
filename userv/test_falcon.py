import falcon
import ujson as json

kv = {}

class KV:
	def on_get(self, req, resp):
		op = req.get_param('op')
		if op=='get':
			k = req.get_param('k')
			v = json.dumps(kv.get(k))
			resp.data = v
		elif op=='set':
			k = req.get_param('k')
			v = req.get_param('v')
			kv[k] = v
			resp.data = json.dumps({'k':k,'v':v})

api = falcon.API()
api.add_route('/kv',KV())

# RUN: waitress-serve test_falcon:api
