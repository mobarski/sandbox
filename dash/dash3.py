## DECLARATIVE AUTOMATION SHELL
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: EX3

## EX3 CHANGES:
## - ability to split long columns into multiple rows
## - pipe and star characters no longer a comment
## - export (to xls) function
## MK2 CHANGES:
## - text after section name -> section hint (one line description)
## - dedent code before splitting it into sections
## - ability to select lines based on first character (to pass metadata in comments)
## - default value changed from None to empty string 

import re
from textwrap import dedent

# TODO complex types -> collect after x cols into list, dict
# TODO rename parse->???
# TODO rename cnt->cols->col_cnt
# TODO control over stripping cells 

p_section = """ (?xms)
	^ \*{3} \s* (.+?) \s* \*{3}	# name
	[ \t]* (.*?) [ \t]* $			# meta
	(.+?) (?= ^ \*{3} | \Z)		# body
"""

p_eol = '\n\r|\r\n|\n|\r'

def parse(text,cnt=0,default='',comments='#<>!@+-',empty='.',select=''):
	"parse body of dash section and return list of values for each row"
	def field(x):
		return x.strip() if x.strip()!=empty else default
	def fields(line):
		if cnt:
			return ([field(x) for x in re.split('\t+',line)]+[default]*cnt)[:cnt]
		else:
			return [field(x) for x in re.split('\t+',line)]

	if select:
		lines = [x.strip() for x in re.split(p_eol,text.strip()) if x.strip() and x.strip()[0] in select]
	else:
		lines = [x.strip() for x in re.split(p_eol,text.strip()) if x.strip() and x.strip()[0] not in comments]

	out = []
	while lines:
		line = lines.pop(0)
		row = fields(line) 
		if '@' in row: # line extension support
			extension = []
			while True:
				if not lines: break
				ext = fields(lines[0])
				if ext[0] != '|': break
				lines.pop(0)
				extension += [ext]
			n = 1
			for i in range(len(row)):
				if row[i]!='@': continue
				row[i] = ' '.join([x[n] for x in extension if len(x)>=n+1])
				n += 1
		out += [row]
	return out

def sections(text):
	"return [name,hint,body] for each section"
	return re.findall(p_section,dedent(text))

def export(text,path):
	f=open(path,'w')
	out = re.sub('\t+','\t',dedent(text))
	f.write(out)

__SCITE_CFG = """
	-- DASH
	file.patterns.diff=$(file.patterns.diff);*.dash
	use.tabs.*.dash=1
	tab.size.*.dash=8
	indent.size.*.dash=8
	fold.flags=0
"""

###################################################


if __name__=="__main__":
	test = """
	*** sekcja ***
		to		@		test		@
		|		jest				raz
		|		pewien			dwa
		|		dosyc			trzy
		|		maly i niezbyt
		|		skomplikowany
		|		(ale i tak moge zajac bardzo duzo z tej jednej linii)
		aaa		bbb		ccc		ddd

	*** costam *** xxx
	@	k1	v1
	@	k2	v2
	>	col1	col2	col3
		a	b	c
	"""
	for name,hint,body in sections(test):
		print(name,parse(body))
	test=open('conceptual.dash','r').read()
	export(test,'dash.test.xls')
