import marshal
from ogonki import remove_ogonki

# http://sgjp.pl/morfeusz/dopobrania.html
# http://nlp.ipipan.waw.pl/CORPUS/znakowanie.pdf
# https://github.com/morfologik/morfologik-stemming/blob/master/morfologik-polish/src/main/resources/morfologik/stemming/polish/polish.README.Polish.txt

# ------------------------------------------------------------------------------

def extract_copyright(f):
	MAX_COPYRIGHT_END_LINE = 100
	copyright = ""
	for i in range(MAX_COPYRIGHT_END_LINE):
		line = f.readline()
		copyright += line
		if line.startswith('#</COPYRIGHT'):
			return copyright
	raise Exception('MAX_COPYRIGHT_END_LINE reached')

def init_dict(out_path, fun, polimorf_path, reduce_fun=None, out_type=dict, out_fun=None):
	f = open(polimorf_path, 'rb')
	copyright = extract_copyright(f)
	out = out_type()
	for line in f:
		line = line.rstrip().decode('utf8').lower()
		word,lem,info0,info1,info2 = (line+'\t\t\t\t').split('\t')[:5]
		#
		fun(out, word,lem,info0,info1,info2)
	out2 = reduce_fun(out) if reduce_fun else out
	# save output
	if out_fun:
		out_fun(out_path,out2) # TODO copyright
	else:
		f_out = open(out_path,'wb')
		marshal.dump(out2, f_out)
		marshal.dump(copyright, f_out)
	
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def name_fun(out, word,lem,info0,info1,info2):
	if not info1: return
	#
	info1 = info1.translate(remove_ogonki)
	if word not in out:
		out[word] = set()
	out[word].update(info1.split('|'))

def lem_fun(out, word,lem,info0,info1,info2):
	if 'brev:'   in info0: return
	if 'part'    in info0: return
	if 'przest.' in info2: return
	#
	if word not in out:
		out[word] = set([lem])
	else:
		out[word].add(lem)

def pos_fun(out, word,lem,info0,info1,info2):
	#
	pos = info0.split(':')[0]
	if word not in out:
		out[word] = set([pos])
	else:
		out[word].add(pos)	

import re
gender_re = re.compile(r'\b(m1|m2|m3|m|n1|n2|n|p1|p2|p3|p|f)\b')
number_re = re.compile(r'\b(pl|sg)\b')
case_re = re.compile(r'\b(nom|gen|acc|dat|inst|loc|voc)\b')
person_re = re.compile(r'\b(pri|sec|ter)\b') # NEW
def multi_fun(out, word,lem,info0,info1,info2):
	# TODO word_raw (not lower)
	pos = info0.split(':')[0]
	case = ','.join(tuple(case_re.findall(info0)))
	gender = ','.join(tuple(gender_re.findall(info0)))
	number = ','.join(tuple(number_re.findall(info0)))
	person = ','.join(tuple(person_re.findall(info0)))
	info1 = info1.translate(remove_ogonki).replace('|',',')
	info2 = info2.translate(remove_ogonki).replace('|',',')
	#
	for c in case.split(','):
		out.add((word,lem,pos,c,number,gender,person,info1,info2))

def multi_sqlite(db_path,out):
	import sqlite3
	import os
	if os.path.exists(db_path): os.remove(db_path)
	db=sqlite3.connect(db_path)
	db.execute('create table xxx (word,lem,pos,case_,number,gender,person,info1,info2)')
	db.executemany('insert into xxx values (?,?,?,?,?,?,?,?,?)',out)
	db.execute('create index ixxx on xxx(word)')
	db.commit()

# ------------------------------------------------------------------------------

def join_out(out):
	return {k:u','.join(out[k]) for k in out} if join else out

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

if __name__=="__main__":
	dict_path = 'polimorf-20190617.tab'
	if 0: init_dict('name.marshal', name_fun, dict_path, reduce_fun=join_out)
	if 0: init_dict('lem.marshal', lem_fun, dict_path, reduce_fun=join_out)
	if 0: init_dict('pos.marshal', pos_fun, dict_path, reduce_fun=join_out)
	if 1: init_dict('multi8.sqlite', multi_fun, dict_path, out_type=set, out_fun=multi_sqlite)
