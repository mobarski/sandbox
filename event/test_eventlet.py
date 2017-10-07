import eventlet
from eventlet.green import urllib2
from time import time

N=500
urls = ['http://www.bing.com/search?q=test{0}'.format(i) for i in range(N)]


def fetch(url):
    return urllib2.urlopen(url).read()

t0=time()
pool = eventlet.GreenPool()
for body in pool.imap(fetch, urls):
    print("got body", len(body))
t1=time()
print(t1-t0,N/(t1-t0))
