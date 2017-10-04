import json,zlib

class Handler:
	def __init__(self):
		self.data = {1:11,2:22,3:33,4:44}
		
	CLASS_BY_TYPE_CODE = {
		'dict':dict,
		'set':set
	}
	
	def serialize(self, obj):
		return json.dumps(obj)
		
	def deserialize(self, s):
		return json.loads(s)
	
	def handle(self, msg):
		resp = 'OK'
		type_code = msg[0]
		op_code = msg[1]
		
		if type_code in self.CLASS_BY_TYPE_CODE:
			key = msg[2]
			if op_code=='init':
				cls = self.CLASS_BY_TYPE_CODE[type_code]
				self.data[key] = cls()
			else:
				obj = self.data[key]
				fun = getattr(obj,op_code,None)
				if fun:
					resp = fun(*msg[3:])
				else:
					pass # TODO helper object/function OR default object wrappers ???
				
		elif type_code in ['db','all','any']:
			fun = getattr(self,'handle_'+type_code)
			resp = fun(msg)
		else:
			resp = 'ERR - unknown type: '+type_code
			
		print(resp)
		return resp
	
	# TODO przerobic na metody
	def handle_db(self,msg):
		op_code = msg[1]
		
		if op_code=='keys':
			return self.data.keys()
			
		elif op_code=='delete':
			for k in msg[2:]:
				if k in self.data:
					del self.data[k]
			return 'OK'
		
		elif op_code=='dump':
			k = msg[2]
			if k in self.data:
				obj = self.data[k]
				resp = self.serialize(obj)
			else:
				resp = None
			return resp
		
		elif op_code=='rename':
			key = msg[2]
			new_key = msg[3]
			if key not in self.data: return 'ERR'
			self.data[new_key] = self.data[key]
			del self.data[key]
			return 'OK'


h = Handler()
h.handle(['db','keys'])
h.handle(['dict','init','d1'])
h.handle(['set','init','s1'])
h.handle(['db','rename','s1','set1'])
h.handle(['db','delete',1,3])
h.handle(['dict','__setitem__','d1','answer',42])
h.handle(['db','keys'])
h.handle(['dict','items','d1'])
h.handle(['db','dump','d1'])
