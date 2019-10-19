import requests

def get_url(n,page=1):
	return "https://lospec.com/palette-list/load?colorNumberFilterType=exact&colorNumber={}&page={}&tag=&sortingType=default".format(n,page)

print(get_url(8,1))
