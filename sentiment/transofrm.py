import re

fi = open('negative.tsv')
fo = open('negative.tsv.txt','w')

for line in fi:
	rec = line.decode('utf8').split('\t')
	notes = rec[-1]
	m = re.findall('\d+',notes)
	cnt = m[0] if m else '-1'
	rec2 = rec[:-1]+[cnt]+[rec[-1]]
	fo.write(u'\t'.join(rec2).encode('utf8'))
