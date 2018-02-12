import urllib2
import re
from hashlib import sha1
from time import time

try:
	from HTMLParser import HTMLParser
except ImportError:
	from html.parser import HTMLParser
h = HTMLParser()

def fetch_text_urls(url,separate_a=False):
	r = urllib2.urlopen(url)
	text = r.read()
	hrefs = set(re.findall('href="[^"]+"',text))
	hrefs |= set(re.findall('http[s]?://[^"]+',text))
	clean = h.unescape(text.decode('utf8'))
	clean = re.sub('(?s)\s+',' ',clean)
	clean = re.sub('(?s)<script.*?</script>',' . ',clean)
	clean = re.sub('(?s)<style.*?</style>',' . ',clean)
	if separate_a==False:
		clean = re.sub('(?s)<a [^>]*?>','  ',clean)
		clean = re.sub('(?s)</a>','  ',clean)
	clean = re.sub('(?s)<[^>]*?>',' . ',clean)
	clean = re.sub('(?s)\s+',' ',clean)
	clean = re.sub('(?s)[ .]{2,}',' . ',clean)
	clean = re.sub('(?s)\s+',' ',clean)
	return clean.strip(),hrefs

if __name__=="__main__":
	## import urls
	## t0 = time()
	## if 1:
		## for topic in urls.topic_urls:
			## for url in urls.topic_urls[topic]:
				## urlid = sha1(url).hexdigest()[:16]
				## print(topic,urlid,url)
				## if urlid in text_db: continue
				## text = fetch_text(url)
				## text_db[urlid] = text
		## text_db.sync()
	## print(list(text_db.keys())[:5])
	## print(time()-t0)
	url = "https://pl.wikipedia.org/wiki/Nikola_Tesla"
	text,urls = fetch_text_urls(url)
	#print(text.encode('utf8'))
	#print(len([u for u in urls if not re.findall('jpg|jpeg|gif|png|svg|ico',u.lower())]))
	text = text.encode('utf8')
	for sentence in text.split('.'):
		if len(sentence.strip().split(' '))<3: continue
		print(sentence.strip())
