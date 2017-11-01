from contrib import *
import urllib3
import re
from hashlib import sha1
from time import time

http = urllib3.PoolManager()
#text_db = text_db('data/text.db',5)
text_db = KO('data/text')
## url_db = text_db('data/url.db',5)

def fetch_text(url):
	r = http.request('GET',url)
	raw = r.data
	clean = raw
	clean = re.sub('\s+',' ',clean)
	clean = re.sub('<script>.*?</script>',' ',clean)
	clean = re.sub('<[^>]*>',' ',clean)
	clean = re.sub('\s+',' ',clean)
	return clean.strip()

if __name__=="__main__":
	import urls
	t0 = time()
	if 1:
		for topic in urls.topic_urls:
			for url in urls.topic_urls[topic]:
				urlid = sha1(url).hexdigest()[:16]
				print(topic,urlid,url)
				if urlid in text_db: continue
				text = fetch_text(url)
				text_db[urlid] = text
		text_db.sync()
	print(list(text_db.keys())[:5])
	print(time()-t0)
