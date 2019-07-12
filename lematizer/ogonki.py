# encoding: utf-8

in_tab = u"ŻÓŁĆĘŚĄŹŃżółćęśąźń"
out_tab = u"ZOLCESAZNzolcesazn"
remove_ogonki = dict(zip([ord(c) for c in in_tab],out_tab))

# 

def replace_polish_letters(text):
	return unicode(text.decode('utf8')).translate(remove_ogonki)
def replace_polish_letters_(text):
	return unicode(text).translate(remove_ogonki)

if __name__=="__main__":
	print(replace_polish_letters('żółć'))
