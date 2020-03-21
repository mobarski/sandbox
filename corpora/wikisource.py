import sqlite3

# TODO: https://archive.org/download/plwiki-20190201 -> 1.6G bz2

# ---[ INIT ]-------------------------------------------------------------------

db = sqlite3.connect('wikisource.sqlite')
db.execute("""
	create table if not exists main (
		key primary key
		,col
		,pos
		,title
		,col_title
		,url
		,text
		,aux
	)
""")

# TODO freq.db -> key,col,token_id,token,freq
# TODO remap freq
# TODO merge freq

# ---[ READ ]-------------------------------------------------------------------

def get_collections():
	results = db.execute('select distinct col,col_title from main').fetchall()
	return dict(results)

def get_titles(col):
	results = db.execute('select key,title from main where col==?',[col]).fetchall()
	return dict(results)

def get_text(key):
	return db.execute('select text from main where key==?',[key]).fetchone()[0]

# ---[ WRITE ]------------------------------------------------------------------

def add_text(col,pos,title,col_title,url,text,aux=''):
	key = '{}{}'.format(col,pos)
	db.execute('insert or replace into main values (?,?,?,?,?,?,?,?)',[key,col,pos,title,col_title,url,text,aux])
	db.commit()

# ---[ MAIN ]-------------------------------------------------------------------

if __name__=="__main__":
	if 0:
		#for x in db.execute('select key,title,length(text),length(aux) from main where key=="DM9"'):
		for x in db.execute('select count(distinct(title)) from main'):
			print(x)
	if 0:
		x = db.execute('select aux from main where key=="DM9"').fetchone()[0]
		print(x[:10000])
	if 0:
		x = get_text('KK1')
		print(x[:1000])
	if 0:
		x = get_collections()
		for k,t in x.items():
			print(k,'=>',t)
	if 0:
		x = get_titles('SC')
		for k,t in x.items():
			print(k,'->',t)
			
	if 1:
		import re
		from collections import Counter
		text = get_text('KK1')
		tokens = re.findall("(?u)[\w]+|[.!?]+|\n",text)
		freq = Counter(tokens)
		print(len(text),len(tokens),len(freq))
		t2i = {t:i+1 for i,(t,f) in enumerate(freq.most_common())}
		for x in freq.most_common(10):
			print(x,t2i[x[0]])
		vec = [t2i.get(t,0) for t in tokens]
		print(vec[:10])
		print(tokens[:10])
		
		


