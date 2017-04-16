import re
from itertools import permutations
from util import normalize

# TODO mleko 2.5 procent
# TODO mak vs maka -> dwa przejscia, najpierw bez usuwania samoglosek potem z
# TODO podobne produkty
# TODO listy slownikow (usera,polprodukty,produkty)
# TODO inne atrybuty np. cena, fodmap, makroskladniki

p_item_value = '(\w[^\d]+?)\s+(\d+)' # TODO negative lookahead \d -> smietana 20% 100

kcal = {}
f = open('kcal.txt','r')
for line in f.readlines():
	line=line.strip()
	if not line or line[0]=='*': continue
	m = re.findall(p_item_value,line)
	if not m: continue
	item,k100 = m[0]
	for p in permutations(re.split('\s+',item)):
		item_key = normalize(' '.join(p))
		#print(item_key)
		kcal[item_key] = int(k100)
f.close()

def licz(text):
	itw_list = re.findall(p_item_value,text)
	sum_k = 0
	sum_w = 0
	out = []
	for it,w in itw_list:
		w=int(w)
		it_key = normalize(it)
		k100 = kcal.get(it_key,0)
		k = int(w*k100/100)
		out += [(it,w,k)]
		sum_k += k
		sum_w += w
	out += [('SUMA',sum_w,sum_k)]
	return out

