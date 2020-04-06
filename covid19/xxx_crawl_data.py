from pprint import pprint
import requests
import re
import json
from math import log

def get_stats(country):
	out = {}
	url = f"https://www.worldometers.info/coronavirus/country/{country}/"
	resp = requests.get(url)
	raw = re.findall("(?sm)series:\s+\[\{.+?data:.+?]", resp.text)
	for serie in raw:
		name = re.findall("name:\s*'(.+?)'",serie)[0]
		data = re.findall("data:\s*(\[.+?\])",serie)[0].replace('null','0')
		data = json.loads(data)
		out[name] = data
	return out


if __name__=="__main__":
	from matplotlib import pyplot as plt
	plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.cm.tab20.colors)
	min_value = 10
	by_country = {}
	min_len = None
	STAT = 'Deaths'
	#for country in ['poland','italy','france','germany','turkey','uk','sweden','romania','bulgaria','czech-republic','us','canada']:
	for country in ['poland','italy','france','germany','turkey','uk','sweden','romania','us','canada']:
		stats = get_stats(country)
		#pprint(stats); exit()
		stat = stats[STAT]
		stat = [x for x in stat if x>=min_value]
		min_len = min(min_len or len(stat), len(stat))
		by_country[country] = stat
		print(country,len(stat),stat)
	for c in by_country:
		stat = by_country[c]
		#stat = stat[:min_len]
		#stat = [a/b for a,b in zip(stat[1:],stat)]
		plt.plot(range(len(stat)), stat, label=c, linewidth=3)
	plt.yscale('log')
	plt.legend()
	plt.title(f'total {STAT.lower()} after {min_value} {STAT.lower()}')
	plt.show()
	