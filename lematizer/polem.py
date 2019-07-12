import marshal
from time import time as now

def analyze(tokens,ops=[]):
	raw_tokens = tokens
	tokens = []
	for i,word in enumerate(raw_tokens):
		t = Token(word)
		t.i = i
		for op in ops:
			setattr(t, op, _dict[op].get(t,''))
		tokens += [t]
	return Doc(tokens)

class Doc(object):
	def __init__(self,tokens=None):
		self.tokens = tokens if tokens is not None else []

class Token(unicode):
	def __init__(self,text):
		self.text = text

# ------------------------------------------------------------------------------


_dict = {}

def load(name,path):
	load_(name,open(path,'rb'))

def load_(name,file):
	t0 = now()
	_dict[name] = marshal.load(file)
	print('DICT_LOAD {} DONE IN {:.2f} s'.format(name,now()-t0))

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

#dict_load('pos','pos.marshal')
#dict_load('gg','gg.marshal')
#dict_load('lem','lem.marshal')
#dict_load('name','name.marshal')

#doc = analyze('jeden bardzo sprytny robak maciej bada niezbyt wysokie morskie fale w ustce'.split(' '),['pos','gg','lem','name'])
#for t in doc.tokens:
#	print(t,t.pos,t.gg,t.lem,t.name)
