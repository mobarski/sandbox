import gevent
import gevent.monkey
import urllib2
from gevent.pool import Pool
from gevent import Timeout
gevent.monkey.patch_all()
from time import time

N=200
urls = ['https://www.bing.com/search?q=test{0}'.format(i) for i in range(N)]

resp = {}
def fetch(url):
	raw = urllib2.urlopen(url).read()
	resp[url] = raw

t0=time()
pool = Pool(10)
for url in urls:
    pool.spawn(fetch, url)
pool.join()
for k,v in resp.items():
	print('got body',len(v))
	
t1=time()
print(t1-t0,N/(t1-t0))