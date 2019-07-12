from __future__ import print_function
import marshal
from time import time

# DOWNLOAD: http://sgjp.pl/morfeusz/dopobrania.html
# INFO: https://github.com/morfologik/morfologik-stemming/blob/master/morfologik-polish/src/main/resources/morfologik/stemming/polish/polish.README.Polish.txt

SRC_DICT_PATH  = '../twitter/dict/polimorf-20190609.tab'

LEM_DICT_PATH  = '../twitter/dict/polimorf_lem.marshal'
POS_DICT_PATH  = '../twitter/dict/polimorf_pos.marshal'
GG_DICT_PATH  = '../twitter/dict/polimorf_gg.marshal'
NAME_DICT_PATH = '../twitter/dict/polimorf_name.marshal'
SEN_DICT_PATH = '../twitter/dict/sen_adj_1k.marshal'

def init_lem():
	SKIP = 32
	lem_by_word = {}

	fi = open(SRC_DICT_PATH,'rb')
	i = 0
	for line in fi:
		i += 1
		if i<=SKIP: continue
		line = line.rstrip().decode('utf8').lower()
		word,lem,info0,info1,info2 = (line+'\t\t\t\t').split('\t')[:5]
		
		if 'brev:' in info0: continue
		if 'part' in info0: continue
		if 'przest.' in info2: continue
		
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


def init_name():
	SKIP = 32
	name_by_word = {}

	fi = open(SRC_DICT_PATH,'rb')
	i = 0
	for line in fi:
		i += 1
		if i<=SKIP: continue
		line = line.rstrip().decode('utf8')
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



def init_pos():
	global name_by_word
	SKIP = 32
	pos_by_word = {}
	name_by_word = marshal.load(open(NAME_DICT_PATH,'rb')) # 'name' tez jako pos

	fi = open(SRC_DICT_PATH,'rb')
	i = 0
	for line in fi:
		i += 1
		if i<=SKIP: continue
		line = line.rstrip().decode('utf8').lower()
		word,lem,info0,info1,info2 = (line+'\t\t\t\t').split('\t')[:5]
		
		pos = info0.split(':')[0]
		
		if word not in pos_by_word:
			pos_by_word[word] = set([pos])
		else:
			pos_by_word[word].add(pos)

		if name(word):
			pos_by_word[word].add('name') # 'name' tez jako pos
			
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

def init_gg():
	SKIP = 32
	gg_by_word = {}

	fi = open(SRC_DICT_PATH,'rb')
	i = 0
	for line in fi:
		i += 1
		if i<=SKIP: continue
		line = line.rstrip().decode('utf8').lower()
		word,lem,info0,info1,info2 = (line+'\t\t\t\t').split('\t')[:5]
		
		info0_set = set(info0.replace('.',':').split(':'))
		gender = info0_set & set(['m','f','n','m1','m2','m3'])
		gender = set([x[0] for x in gender]) # m f n
		gg = set()
		for g in gender:
			if 'sg' in info0_set:
				gg.add('s'+g)
			if 'pl' in info0_set:
				gg.add('p'+g)
		
		if word not in gg_by_word:
			gg_by_word[word] = gg
		else:
			gg_by_word[word].update(gg)
			
	out = {}
	for word in gg_by_word:
		out[word] = ','.join(gg_by_word[word])
	
	marshal.dump(out,open(GG_DICT_PATH,'wb'))

if 1:
	t0 = time()
	#lem_by_word = marshal.load(open(LEM_DICT_PATH,'rb'))
	pos_by_word = marshal.load(open(POS_DICT_PATH,'rb'))
	gg_by_word = marshal.load(open(GG_DICT_PATH,'rb'))
	sen_by_word = marshal.load(open(SEN_DICT_PATH,'rb'))
	#name_by_word = marshal.load(open(NAME_DICT_PATH,'rb'))
	print("dictionaries loaded in {} seconds (pos,gg,sen)".format(int(time()-t0))) # 10s

def lematize(word):
	return lem_by_word.get(word,word)

def pos(word):
	return pos_by_word.get(word,'')

def name(word):
	return name_by_word.get(word,'')

def gg(word):
	return gg_by_word.get(word,'')

def sen(word):
	return sen_by_word.get(word,'')

if __name__=="__main__":
	#init_lem()
	#init_name()
	#init_pos()
	#init_gg()
	pass
	#for w in ['malowana','szybka','szybki','szybkie']: print(w,gg(w))





