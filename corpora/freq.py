import re
from collections import Counter

# TODO model(tokens) vs model(freq)

class model:

	def __init__(self,tokens):
		self.token_freq = Counter(tokens)
		self.recalc_ids()
	
	def recalc_ids(self):
		freq = self.token_freq
		self.token2id = {t:i+1 for i,(t,f) in enumerate(freq.most_common())}
		self.id2token = {i:t for t,i in self.token2id.items()}
		t2i = self.token2id
		self.id_freq = {t2i[t]:f for i,(t,f) in enumerate(freq.most_common())}
	
	def encode(self,tokens):
		get = self.token2id.get
		return [get(t,0) for t in tokens]
	
	def decode(self,ids):
		get = self.id2token.get
		return [get(i,'___') for i in ids]

	def merge(self,other):
		pass # TODO
	
	def merge_freq(self,token_freq):
		"requires calling to recalc_ids"
		self.token_freq.update(token_freq)
	
	def add(self,tokens):
		delta = model(tokens)
		self.merge(delta)

# ---[

import sqlite3
db = sqlite3.connect('freq.sqlite')
db.execute("""
	create table if not exists freq (
		key
		,col
		,id
		,token
		,freq
	)
""")

db.execute("""create index if not exists i_freq on freq (key)""")
db.commit()

def save_freq(key,col,m):
	get = m.token_freq.get
	values = [(key,col,i,t,get(t)) for i,t in sorted(m.id2token.items())]
	db.execute('delete from freq where key==?',[key])
	db.executemany('insert into freq values (?,?,?,?,?)',values)
	db.commit()

# ---[ MAIN ]-------------------------------------------------------------------

if __name__=="xxx__main__":
	import wikisource as corpus
	from time import time
	
	t0=time()
	text = corpus.get_text('KK1')
	tokens = re.findall("(?u)[\w]+|[.!?]+|\n",text)
	t1=time()
	m = model(tokens)
	vec = m.encode(tokens)
	t2=time()
	print(t1-t0)
	print(t2-t1)
	print(t2-t0)
	
	for x in m.token_freq.most_common(10):
		print(x,m.token2id[x[0]])
	print(tokens[:10])
	print(vec[:10])
	print(m.decode(vec[:10]))


if __name__=="__main__":
	import wikisource as corpus
	from time import time
	import sys
	
	for col in corpus.get_collections():
		for key,title in corpus.get_titles(col).items():
			print(key,title);sys.stdout.flush()
			text = corpus.get_text(key)
			tokens = re.findall("(?u)[\w]+|[.!?]+|\n",text)
			m = model(tokens)
			save_freq(key,col,m)
