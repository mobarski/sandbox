import marshal
import re

def get_sentences(text,min_len=3):
	for sentence in re.split('[.!?;]',text):
		if len(sentence.strip().split(' '))<min_len: continue
		yield sentence

def sentences_iter(path,min_len=1):
	pages = marshal.load(open(path,'rb'))
	for url,text in pages.items():
		for x in get_sentences(text,min_len):
			yield x

def print_count():
	scnt = 0
	pages = marshal.load(open('onet_text.mrl','rb'))
	for url,text in pages.items():
		s = len(list(get_sentences(text,20)))
		scnt += s
		print(len(text),s,url)
		#for x in get_sentences(text,20): print(x)
	print(scnt)	

if __name__=="__main__":
	for x in sentences_iter('onet_text.mrl',20):
		print(x)
