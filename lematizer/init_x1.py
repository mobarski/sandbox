import marshal
from ogonki import remove_ogonki

# http://download.sgjp.pl/morfeusz/
# http://nlp.ipipan.waw.pl/CORPUS/znakowanie.pdf
# https://github.com/morfologik/morfologik-stemming/blob/master/morfologik-polish/src/main/resources/morfologik/stemming/polish/polish.README.Polish.txt

# TODO - rename xxx
# TODO - info1 / info2 as json

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

def init_dict(polimorf_path, out_path, collect_fun, reduce_fun=None, out_type=dict, out_fun=None):
	f = open(polimorf_path, 'rb')
	copyright = extract_copyright(f)
	out = out_type()
	for line in f:
		line = line.rstrip().decode('utf8')
		word,lem,info0,info1,info2 = (line+'\t\t\t\t').split('\t')[:5]
		#
		collect_fun(out, word,lem,info0,info1,info2)
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

# OLD
def collect_name(out, word,lem,info0,info1,info2):
	if not info1: return
	#
	info1 = info1.translate(remove_ogonki)
	if word not in out:
		out[word] = set()
	out[word].update(info1.split('|'))

# OLD
def collect_lem(out, word,lem,info0,info1,info2):
	if 'brev:'   in info0: return
	if 'part'    in info0: return
	if 'przest.' in info2: return
	#
	if word not in out:
		out[word] = set([lem])
	else:
		out[word].add(lem)

# OLD
def collect_pos(out, word,lem,info0,info1,info2):
	#
	pos = info0.split(':')[0]
	if word not in out:
		out[word] = set([pos])
	else:
		out[word].add(pos)	

pos_by_flex = {
	'subst':'rzeczownik',
	'depr':'rzeczownik',
	'adj':'przymiotnik',
	'adja':'przymiotnik',
	'adjp':'przymiotnik',
	'adv':'przyslowek',
	'num':'liczebnik',
	'ppron12':'zaimek',
	'ppron3':'zaimek',
	'siebie':'zaimek',
	'fin':'czasownik',
	'bedzie':'czasownik',
	'aglt':'czasownik',
	'praet':'czasownik',
	'impt':'czasownik',
	'imps':'czasownik',
	'inf':'czasownik',
	'pcon':'czasownik',
	'pant':'czasownik',
	'ger':'czasownik',
	'pact':'czasownik',
	'ppas':'czasownik',
	'winien':'czasownik',
	'pred':'predykatyw',
	'prep':'przyimek',
	'conj':'spojnik',
	'qub':'kublik',
	'xxs':'cialo_obce',
	'xxx':'cialo_obce',
}

import re
gender_re = re.compile(r'\b(m1|m2|m3|m|n1|n2|n|p1|p2|p3|p|f)\b')
number_re = re.compile(r'\b(pl|sg)\b')
case_re = re.compile(r'\b(nom|gen|acc|dat|inst|loc|voc)\b')
person_re = re.compile(r'\b(pri|sec|ter)\b')
neg_re = re.compile(r'\b(aff|neg)\b') # NEW
degree_re = re.compile(r'\b(pos|comp|sup)\b') # NEW
aspect_re = re.compile(r'\b(imperf|perf)\b') # NEW

def collect_all(out, word,lem,info0,info1,info2):
	word_lower = word.lower()
	flex = info0.split(':')[0]
	pos = pos_by_flex.get(flex)
	case = ','.join(tuple(case_re.findall(info0)))
	gender = ','.join(tuple(gender_re.findall(info0)))
	number = ','.join(tuple(number_re.findall(info0)))
	person = ','.join(tuple(person_re.findall(info0)))
	neg = ','.join(tuple(neg_re.findall(info0))) # NEW
	aspect = ','.join(tuple(aspect_re.findall(info0))) # NEW
	degree = ','.join(tuple(degree_re.findall(info0))) # NEW
	info1 = info1.translate(remove_ogonki).replace('|',',')
	info2 = info2.translate(remove_ogonki).replace('|',',').replace('.','')
	#
	for c in case.split(','):
		out.add((word,word_lower,lem,pos,flex,c,number,gender,person,neg,aspect,degree,info1,info2))

def sqlite_output(db_path,out):
	import sqlite3
	import os
	if os.path.exists(db_path): os.remove(db_path)
	db=sqlite3.connect(db_path)
	sql = 'create table xxx (word,word_lower,lem,pos,flex,case_,number,gender,person,neg,aspect,degree,info1,info2)'
	db.execute(sql)
	n_cols = len(re.findall(',',sql))+1
	placeholders = ','.join(['?']*n_cols)
	db.executemany('insert into xxx values ({})'.format(placeholders),out)
	db.execute('create index ixxx_word on xxx(word)')
	db.execute('create index ixxx_word_lower on xxx(word_lower)')
	db.commit()

# ------------------------------------------------------------------------------

# OLD
def join_out(out):
	return {k:u','.join(out[k]) for k in out} if join else out

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

if __name__=="__main__":
	from time import time
	t0 = time()
	dict_path = 'polimorf-20191229.tab'
	if 0: init_dict(dict_path, 'name.marshal',  collect_name, reduce_fun=join_out)
	if 0: init_dict(dict_path, 'lem.marshal',   collect_lem,  reduce_fun=join_out)
	if 0: init_dict(dict_path, 'pos.marshal',   collect_pos,  reduce_fun=join_out)
	if 1: init_dict(dict_path, 'multi9.sqlite', collect_all, out_type=set, out_fun=sqlite_output)
	print('DONE in {:.0f}s'.format(time()-t0))
