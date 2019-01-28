#encoding: utf8
from __future__ import print_function
import marshal
from time import time

# DOWNLOAD: http://sgjp.pl/morfeusz/dopobrania.html
# INFO: https://github.com/morfologik/morfologik-stemming/blob/master/morfologik-polish/src/main/resources/morfologik/stemming/polish/polish.README.Polish.txt


SRC_DICT_PATH = '../data/polimorf-20190120.tab'
LEM_DICT_PATH = '../data/polimorf_lem.marshal'
POS_DICT_PATH = '../data/polimorf_pos.marshal'
NAME_DICT_PATH = '../data/polimorf_name.marshal'

in_tab = u"ŻÓŁĆĘŚĄŹŃżółćęśąźń"
out_tab = u"ZOLCESAZNzolcesazn"
tran_map = dict(zip([ord(c) for c in in_tab],out_tab))
def replace_polish_letters(text):
	return unicode(text.decode('utf8')).translate(tran_map)

def init_lem(replace_pl=False):
	SKIP = 32
	lem_by_word = {}

	fi = open(SRC_DICT_PATH,'rb')
	i = 0
	for line in fi:
		i += 1
		if i<=SKIP: continue
		line = line.rstrip().decode('utf8').lower()
		if replace_pl:
			line = replace_polish_letters(line)
		word,lem,info0,info1,info2 = (line+'\t\t\t\t').split('\t')[:5]

		if word not in lem_by_word:
			lem_by_word[word] = set([lem])
		else:
			lem_by_word[word].add(lem)
	
	out = {}
	single = multiple = 0
	for word in lem_by_word:
		if len(lem_by_word[word])==1:
			single += 1
			#out[word] = list(lem_by_word[word])[0]
		else:
			multiple += 1
		out[word] = u'/'.join(lem_by_word[word])
	
	marshal.dump(out,open(LEM_DICT_PATH,'wb'))
	print('LEM single={}  multiple={}'.format(single,multiple))


def init_pos(replace_pl=False):
	SKIP = 32
	pos_by_word = {}

	fi = open(SRC_DICT_PATH,'rb')
	i = 0
	for line in fi:
		i += 1
		if i<=SKIP: continue
		line = line.rstrip().decode('utf8').lower()
		if replace_pl:
			line = replace_polish_letters(line)
		word,lem,info0,info1,info2 = (line+'\t\t\t\t').split('\t')[:5]
		
		pos = info0.split(':')[0]
		
		if word not in pos_by_word:
			pos_by_word[word] = set([pos])
		else:
			pos_by_word[word].add(pos)

		if name(word):
			pos_by_word[word].add('name')
			
	out = {}
	single = multiple = 0
	for word in pos_by_word:
		if len(pos_by_word[word])==1:
			single += 1
		else:
			multiple += 1
		out[word] = ','.join(pos_by_word[word])
	
	marshal.dump(out,open(POS_DICT_PATH,'wb'))
	print('POS single={}  multiple={}'.format(single,multiple))

def init_name(replace_pl=False):
	SKIP = 32
	name_by_word = {}

	fi = open(SRC_DICT_PATH,'rb')
	i = 0
	for line in fi:
		i += 1
		if i<=SKIP: continue
		line = line.rstrip().decode('utf8')
		if replace_pl:
			line = replace_polish_letters(line)
		word,lem,info0,info1,info2 = (line+'\t\t\t\t').split('\t')[:5]

		if word[0].islower(): continue
		word = word.lower()
		
		if word not in name_by_word:
			name_by_word[word] = set([lem])
		else:
			name_by_word[word].add(lem)
	
	out = {}
	single = multiple = 0
	for word in name_by_word:
		if len(name_by_word[word])==1:
			single += 1
		else:
			multiple += 1
		out[word] = u'/'.join(name_by_word[word])
	
	marshal.dump(out,open(NAME_DICT_PATH,'wb'))
	print('NAME single={}  multiple={}'.format(single,multiple))
	
t0 = time()	
if 0: lem_by_word = marshal.load(open(LEM_DICT_PATH,'rb'))
if 0: pos_by_word = marshal.load(open(POS_DICT_PATH,'rb'))
if 0: name_by_word = marshal.load(open(NAME_DICT_PATH,'rb'))
print("dictionaries loaded in {} seconds (lem,pos,name)".format(int(time()-t0))) # 10s

def lematize(word,replace_pl=False):
	if replace_pl:
		word = replace_polish_letters(word)
	return lem_by_word.get(word,word)

def pos(word,replace_pl=False):
	if replace_pl:
		word = replace_polish_letters(word)
	return pos_by_word.get(word,'')

def name(word,replace_pl=False):
	if replace_pl:
		word = replace_polish_letters(word)
	return name_by_word.get(word,'')
	
if __name__=="__main__":
	#init_lem()
	#init_pos()
	#init_name()
	pass
