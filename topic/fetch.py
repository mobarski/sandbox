from contrib import *
import urllib3
import re
from zlib import compress
from hashlib import sha1
from time import time

http = urllib3.PoolManager()
kv = KV('data/urlid_text.db',5,tab=1)

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
	if 0:
		for topic in urls.topic_urls:
			for url in urls.topic_urls[topic]:
				urlid = sha1(url).hexdigest()[:16]
				print(topic,urlid,url)
				text = fetch_text(url)
				kv[urlid] = text
			kv.commit()
	print(list(kv.keys(limit=5)))
	print(time()-t0)

