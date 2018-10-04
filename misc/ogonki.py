# encoding: utf-8

in_tab = u"ŻÓŁĆĘŚĄŹŃżółćęśąźń"
out_tab = u"ZOLCESAZNzolcesazn"
tran_map = dict(zip([ord(c) for c in in_tab],out_tab))
def replace_polish_letters(text):
	return unicode(text.decode('utf8')).translate(tran_map)

if __name__=="__main__":
	print(replace_polish_letters('żółć'))
