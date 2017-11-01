from contrib import *

if 1:
	db = KCV('data/text.kcv')
	if 0:
		text = KV('data/text.db',5)
		for k,v in text.items():
			db.set('text',k,v.decode('utf8'))
		db.sync()
	db.to_col_store('data/text_col.kcv',batch=10)

if 1:
	db = KCV('data/tokens.kcv')
	if 1:
		text = KV('data/tokens.db',5)
		for k,v in text.items():
			db.set('tokens',k.decode('utf8'),v)
		db.sync()
	db.to_col_store('data/tokens_col.kcv',batch=10)
