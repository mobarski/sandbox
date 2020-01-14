import requests
import re
from urllib.parse import unquote
from zlib import crc32
from time import sleep

url_list = {
'DM':'https://pl.wikisource.org/wiki/Kolekcja:Literatura_dla_dzieci_i_młodzieży',
'PH':'https://pl.wikisource.org/wiki/Kolekcja:Powieści_historyczne',
'PM':'https://pl.wikisource.org/wiki/Kolekcja:Polska_powieść_międzywojenna',
'SC':'https://pl.wikisource.org/wiki/Kolekcja:W_poszukiwaniu_straconego_czasu',
'US':'https://pl.wikisource.org/wiki/Kolekcja:Literatura_amerykańska',
'BB':'https://pl.wikisource.org/wiki/Kolekcja:Biblioteka_Boya',
'CP':'https://pl.wikisource.org/wiki/Kolekcja:Cykle_powieściowe',
'DE':'https://pl.wikisource.org/wiki/Kolekcja:Literatura_niemiecka',
'RU':'https://pl.wikisource.org/wiki/Kolekcja:Literatura_rosyjska',
'SM':'https://pl.wikisource.org/wiki/Kolekcja:Skarbnica_Milusińskich',
'FR':'https://pl.wikisource.org/wiki/Kolekcja:Literatura_francuska',
'KK':'https://pl.wikisource.org/wiki/Kolekcja:Książki_kulinarne',
'UK':'https://pl.wikisource.org/wiki/Kolekcja:Literatura_angielska',
'FN':'https://pl.wikisource.org/wiki/Kolekcja:Fantastyka_naukowa',
}

def get_title(url):
	return url.split('/wiki/')[-1]

def get_local_urls(url):
	r = requests.get(url)
	text = r.text
	links = sorted(set(re.findall('/wiki/[^"]+',text)))
	out = []
	for x in links:
		if re.findall(':|cookie|privacy|warunki_korzystania',x.lower()): continue
		#x = unquote(x)
		out += [x]
	return out

def clean(text):
	text = re.sub('<[^>]+>','',text) # html
	text = re.sub('&#\d+;','',text) # ???
	text = re.sub('\[\d+\]','',text) # przypisy w tekscie
	text = re.sub('(?m)^↑.*$','',text) # przypisy na koncu
	if 'nie ma jeszcze tekstu o tytule' in text and 'pl.wikisource.org' in text:
		return ''
	else:
		return text

def get_raw_text(local_url,method=''):
	print('.',end=''); sys.stdout.flush()
	url = 'https://pl.wikisource.org{}{}'.format(local_url,method)
	#print('XXX getting url: {}'.format(url))
	r = requests.get(url)
	text = r.text
	#text = re.split("prp-pages-output[^>]+>",text)[-1]
	text = re.split("prp-pages-output[^>]+>",text,1)[-1]
	text = re.split("<[^>]+Template_law",text)[0]
	return text


def get_part_urls(raw):
	out = []
	for x in re.findall('/wiki/[^/":]+/[^"]+',raw):
		if x.count('/')>3: continue
		if x in out: continue
		out.append(x)
	return out

# ---

if __name__=="__main__":
	import storage
	import sys
	for col,url in url_list.items():
		#if col not in ['SM']: continue
		for i,local_url in enumerate(get_local_urls(url)):
			title = get_title(local_url)
			pos = i+1
			#if pos not in [75]: continue
			key = '{}{}'.format(col,pos)
			print(key,col,pos,unquote(title),end=' ')
			sys.stdout.flush()
			method_list = ['/całość','/Całość','']
			if col in ['SM']:
				method_list = ['']
			
			# CRAWL
			for method in method_list:
				raw = get_raw_text(local_url,method)
				text = clean(raw)
				if len(text)>0:
					break
			
			# AUX
			part_urls = get_part_urls(raw)
			aux = '\n'.join([unquote(x) for x in part_urls])
			
			# PARTS
			if len(text)<30000 and ('/Tom_' in aux or '/01' in aux or '/Część' in aux or len(aux)>len(text)):
				print(len(text),end=' ')
				method_list = ['']
				if '/Tom_' in aux or '/Część' in aux:
					method_list = ['/całość','/Całość','']
				parts = []
				for part_url in part_urls:
					for method in method_list:
						raw = get_raw_text(part_url, method)
						text = clean(raw)
						if len(text)>0:
							break
					parts.append(text)
				text = '----------\n\n'.join(parts)
			print('',len(text));sys.stdout.flush()
			
			# STORE
			storage.add_text(col,pos,unquote(title),text,aux)
		print()
