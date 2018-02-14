import urllib2
import re
from hashlib import sha1
from time import time
import marshal

try:
	from HTMLParser import HTMLParser
except ImportError:
	from html.parser import HTMLParser
h = HTMLParser()

def fetch(url):
	print('FETCH',url)
	r = urllib2.urlopen(url)
	raw = r.read()
	return raw

def get_urls(text):
	"extract urls from html/js"
	hrefs = set()
	urls = [u[0] for u in re.findall('href="([^"]+)"',text)]
	hrefs |= set()
	hrefs |= set(re.findall('http[s]?://[^"]+',text))
	return hrefs

def get_text(text,separate_a=False):
	"extract text from html"
	try:
		clean = text.decode('utf8')
	except:
		clean = text.decode('iso-8859-2')
	clean = h.unescape(clean)
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
	return clean.strip().encode('utf8')

def spider(url,depth=1,allow='',omit=None):
	out = {}
	raw = fetch(url)
	out[url] = raw
	urls = get_urls(raw)
	filtered_urls = []
	for u in urls:
		if u in out: continue
		if not re.findall(allow,u): continue
		if omit and re.findall(omit,u): continue
		filtered_urls += [u]
	
	for i,u in enumerate(filtered_urls):
		try:
			out[u] = fetch(u)
			print('OK {}/{}/{} {}'.format(i+1,len(filtered_urls),len(urls),u))
		except Exception as e:
			print('ERROR',i,u,e)
	return out

if __name__=="__main__":
	if 0:
		url = "https://pl.wikipedia.org/wiki/Nikola_Tesla"
		#urlid = sha1(url.lower()).hexdigest()[:16]
		raw = fetch(url)
		text = get_text(raw)
		urls = get_urls(raw)
		#print(text.encode('utf8'))
		print(len([u for u in urls if not re.findall('(?i)jpg|jpeg|gif|png|svg|ico',u)]))
	if 0:
		url = "https://pl.wikipedia.org/wiki/Nikola_Tesla"
		spider(url,allow='(?i)//(pl|en|simple).wiki(pedia|quote).org',omit='oldid')
	if 0:
		url = "http://onet.pl"
		t0=time()
		out = spider(url,allow='http[s]?://\w+.onet.pl')
		print(time()-t0)
		t1=time()
		marshal.dump(out,open('onet_raw.mrl','wb'))
		print(time()-t1)
	if 0:
		out = {}
		pages = marshal.load(open('onet_raw.mrl','rb'))
		for url,raw in pages.items():
			text = get_text(raw)
			out[url] = text
		marshal.dump(out,open('onet_text.mrl','wb'))


