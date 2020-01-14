import sqlite3

db = sqlite3.connect('corpora.sqlite')
#db.execute("drop table if exists wikisource")
db.execute("""
	create table if not exists wikisource (
		key primary key
		,col
		,pos
		,title
		,text
		,aux
	)
""")

def add_text(col,pos,title,text,aux=''):
	key = '{}{}'.format(col,pos)
	db.execute('insert or replace into wikisource values (?,?,?,?,?,?)',[key,col,pos,title,text,aux])
	db.commit()

if __name__=="__main__":
	if 1:
		#for x in db.execute('select key,title,length(text),length(aux) from wikisource where key=="DM9"'):
		for x in db.execute('select count(distinct(title)) from wikisource'):
			print(x)
	if 1:
		x = db.execute('select aux from wikisource where key=="DM9"').fetchone()[0]
		print(x[:10000])

