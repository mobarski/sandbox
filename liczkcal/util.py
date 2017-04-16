# encoding utf-8

import string

def maketrans(frm,to):
	return(dict(zip(map(ord,frm),to)))

pl_tab = maketrans("żółćęśąźń","zolcesazn")

def normalize(text):
	if len(text)==0: return text
	text = text.strip()
	text = text.lower()
	text = text.translate(pl_tab)
	text = text[:-1] if text[-1] in 'aeiouy' else text
	return text

if __name__=="__main__":
	print(normalize('jajka'))
	print(normalize('jajko'))