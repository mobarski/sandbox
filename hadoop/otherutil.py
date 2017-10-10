# encoding: utf-8

in_tab = u"ŻÓŁĆĘŚĄŹŃżółćęśąźń"
out_tab = u"ZOLCESAZNzolcesazn"
tran_map = dict(zip([ord(c) for c in in_tab],out_tab))
def replace_polish_letters(text):
	return unicode(text.decode('utf8')).translate(tran_map)

def myhash(s):
	return "{:x}".format(abs(hash(s)))

from itertools import izip_longest
def grouper(iterable, n):
	args = [iter(iterable)] * n
	for group in izip_longest(fillvalue=None, *args):
		yield [x for x in group if x is not None]

if __name__=="__main__":
	for x in grouper([1,2,3,4,5,6,7,8,9,10],3):
		print(x)
	print(replace_polish_letters('żółć'))
