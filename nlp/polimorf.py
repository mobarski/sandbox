
def get_lem_dict(path):
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

if __name__=="__main__":
	import marshal
	lem_dict = get_lem_dict('polimorf-20181021.tab')
	marshal.dump(lem_dict,open('lem_dict.mrl','wb'))
