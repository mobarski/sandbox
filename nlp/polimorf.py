"""Creation of dictionaries (word to lemma, word to POS) based on Morfeusz 2
http://sgjp.pl/morfeusz/dopobrania.html
"""

from collections import Counter
import re

def get_lem_dict(path):
	"""Create mapping from word to lemma
	"""
	SKIP = 32
	lem_by_word = {}
	
	uncommon = set()
	uncommon_re = re.compile('daw[.]|przest[.]|rzad[.]|gwar[.]')

	fi = open(path,'rb')
	i = 0
	for line in fi:
		i += 1
		if i<=SKIP: continue
		line = line.rstrip().decode('utf8').lower()
		word,lem,info0,info1,info2 = (line+'\t\t\t\t').split('\t')[:5]

		if word not in lem_by_word:
			lem_by_word[word] = set([lem])
		else:
			lem_by_word[word].add(lem)
		
		if uncommon_re.findall(info1):
			uncommon.add(lem)
	
	
	# minimize conflicts by removing uncommon lemmas if common one is present
	out = {}
	for word in lem_by_word: 
		lemmas = lem_by_word[word]
		common = lemmas - uncommon
		if not common:
			out[word] = u'/'.join(lemmas)
		else:
			out[word] = u'/'.join(common)
	
	return out

def get_stats(path):
	"""
	"""
	SKIP = 32
	i1 = Counter()
	i2 = Counter()
	i3 = Counter()
	

	fi = open(path,'rb')
	i = 0
	for line in fi:
		i += 1
		if i<=SKIP: continue
		line = line.rstrip().decode('utf8').lower()
		word,lem,info0,info1,info2 = (line+'\t\t\t\t').split('\t')[:5]
		
		for x in info0.split('|'):
			i1[x] += 1
		for x in info1.split('|'):
			i2[x] += 1
		for x in info2.split('|'):
			i3[x] += 1
		
	return i1,i2,i3

def scan_dict(path,pattern):
	SKIP = 32

	fi = open(path,'rb')
	i = 0
	for line in fi:
		i += 1
		if i<=SKIP: continue
		line = line.rstrip().decode('utf8').lower()
		word,lem,info0,info1,info2 = (line+'\t\t\t\t').split('\t')[:5]
		if pattern in info2:
			print(word,lem,info0,info1,info2)

if __name__=="__main__":
	import marshal
	if 1:
		lem_dict = get_lem_dict('data/polimorf-20181118.tab')
		marshal.dump(lem_dict,open('data/lem_dict.mrl','wb'))
	if 0:
		# old
		i0a,i1a,i2a = get_stats('data/polimorf-20181021.tab')
		# new
		print
		i0b,i1b,i2b = get_stats('data/polimorf-20181118.tab')
		print(i0b)
		print(i1b)
		print(i2b)
		# compare
		print
		print(i0b-i0a)
		print(i1b-i1a)
		print(i2b-i2a)
	if 0:
		scan_dict('data/polimorf-20181118.tab','przest.')
