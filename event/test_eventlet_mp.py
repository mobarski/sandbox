import eventlet
from eventlet.green import urllib2
from time import time
from multiprocessing import Pool
from itertools import izip_longest,izip


N=500
W=2
urls = ['http://www.bing.com/search?q=test{0}'.format(i) for i in range(N)]

def grouper(iterable, n):
    args = [iter(iterable)] * n
    groups = izip_longest(*args,fillvalue=None)
    return [[x for x in g if x] for g in groups]


def proc_body(urls):
	def fetch(url):
	    return urllib2.urlopen(url).read()
	pool = eventlet.GreenPool()
	for body in pool.imap(fetch, urls):
	    print("got body", len(body))

t0=time()
pool = Pool(W)
grouped_urls = grouper(urls,N/W)
pool.map(proc_body,grouped_urls,N/W)

t1=time()
print(t1-t0,N/(t1-t0))
