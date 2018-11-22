from boardgamegeek import BGGClient
from cache import disk_cache
import marshal

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

VERBOSE = False
#for id in [72125]: # eclipse
#for id in list(ids)[:10]:
#for id in list(ids)[:10]:
for id in ids:
	print(id)
	if cache.has('data',str(id)): continue
	try:
		g = bgg.game(game_id=id)
	except:
		continue
	data = g._data
	if VERBOSE:
		for k,v in data.items():
			print(k,v)
	cache.set_map('data',{str(data['id']):data})
