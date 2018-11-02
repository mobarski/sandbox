"""Creation of dictionaries (word to lemma, word to POS).
"""

def get_lem_dict(path):
	"""Create mapping from word to lemma
	"""
	SKIP = 32
	lem_by_word = {}

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
	
	out = {}
	for word in lem_by_word:
		out[word] = u'/'.join(lem_by_word[word])
	
	return out

def get_stats(path):
	"""
	"""
	SKIP = 32
	i1_set = set()
	i2_set = set()
	i3_set = set()

	fi = open(path,'rb')
	i = 0
	for line in fi:
		i += 1
		if i<=SKIP: continue
		line = line.rstrip().decode('utf8').lower()
		word,lem,info0,info1,info2 = (line+'\t\t\t\t').split('\t')[:5]

		i1_set.add(info0)
		i2_set.add(info1)
		i3_set.add(info2)
		
	return i1_set,i2_set,i3_set

if __name__=="__main__":
	import marshal
	if 0:
		lem_dict = get_lem_dict('../data/polimorf-20181021.tab')
		marshal.dump(lem_dict,open('../data/lem_dict.mrl','wb'))
	if 0:
		i0,i1,i2 = get_stats('../data/polimorf-20181021.tab')
		print(i0)
		print(i1)
		print(i2)
