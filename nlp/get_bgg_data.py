from boardgamegeek import BGGClient
from cache import disk_cache
import marshal
from time import time

# eclipse: 72125

bgg = BGGClient()
cache = disk_cache('cache/bgg',verbose=True)

if 0:
	ids = set()
	for q in "abcdefghijklmnopqrstuvwxyz 1234567890:-.":
		resp = bgg.search(q)
		print(q,len(resp))
		for x in resp:
			ids.add(x.id)
	cache.set('ids',ids)
else:
	ids = cache.get('ids')

if 0:
	N = 1
	todo = []
	for i,id in enumerate(ids):
		if cache.has('data',str(id)): continue
		todo += [id]
		if len(todo)<N: continue
		
		t0=time()
		try:
			g_list = bgg.game_list(todo)
		except:
			continue
		todo = []
		for g in g_list:
			data = g._data
			cache.set_map('data',{str(data['id']):data})
		print(1.0*N/(time()-t0))

if 0:
	t0=time()
	m=cache.get_map('data') # 50s
	cache.set('games',m)
	print(time()-t0)

if 1:
	games = cache.get('games')
	print games['72125']
