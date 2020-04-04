from pprint import pprint
import requests
import re
import json

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
	pprint(get_stats('poland'))
