## DECLARATIVE AUTOMATION SHELL
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: EX6


## EX6 CHANGES:
## - reading from files and paths
## - high level interface for tables
## - high level interfece for rows with column metadata
## - medium level interface for metadata
## - parse changed to generator
## MK5 CHANGES:
## - spliting long columns into multiple rows NOT AVAILABLE - requires rework
## - tail option
## EX4 CHANGES:
## - fixed cnt argument
## - tsv format, multiple tabulators no longer treated as one
## - comments replaced by selectors 
## - lines are no longer stripped (only rstripped)
## - fields stripping can now be turned off
## - removed export function (not needed - dash files can now be edited in excel)
## EX3 CHANGES:
## - ability to split long columns into multiple rows
## - pipe and star characters no longer a comment
## - export (to xls) function
## MK2 CHANGES:
## - text after section name -> section hint (one line description)
## - dedent code before splitting it into sections
## - ability to select lines based on first character (to pass metadata in comments)
## - default value changed from None to empty string 

#####################################################################

import re
from textwrap import dedent

# TODO line extension
# TODO empty -> null
# TODO complex types -> collect after x cols into list, dict
# TODO rename parse->???
# TODO rename cnt->cols->col_cnt

p_section = """ (?xms)
	^ \*{3} \s* (.+?) \s* \*{3}	# name
	[ \t]* (.*?) [ \t]* $			# meta
	(.+?) (?= ^ \*{3} | \Z)		# body
"""

p_eol = '\n\r|\r\n|\n|\r'
p_sep = '\t'

## low level interfece #####################################################

def parse(text,cnt=0,default='',empty='.',select='',strip=True,tail=''):
	"parse body of dash section and return list of values for each row"
	def field(x):
		x = x.strip() if strip else x
		return x if x!=empty else default
		
	def fields(line):
		if cnt:
			return ([field(x) for x in re.split(p_sep,line)]+[default]*cnt) # TODO
		else:
			return [field(x) for x in re.split(p_sep,line)]

	if select:
		lines = [x.rstrip() for x in re.split(p_eol,text) if x.strip() and x[0] in select]
	else:
		lines = [x.rstrip() for x in re.split(p_eol,text) if x.strip() and x[0]=='\t']

	while lines:
		line = lines.pop(0)
		row = fields(line)
		if select:
			if cnt:
				row = row[:cnt]
		else:
			row = row[1:] # skip first column
			if cnt:
				if tail:
					tail_list = [x for x in row[cnt-1:] if x]
					if tail=='list':
						row = row[:cnt-1]+[tail_list]
					elif tail=='dict':
						d = dict([x.partition(':')[::2] for x in tail_list])
						row = row[:cnt-1]+[d]
					else:
						raise
				else:
					row = row[:cnt]
		# TODO support of line extension
		yield row

def sections(text):
	"return [name,hint,body] for each section"
	return re.findall(p_section,dedent(text))

## medium level interface ################################

def get_meta(text,select="+",strip=False):
	if strip:
		return [(r[0][1:],r[1:]) for r in parse(text,select=select)]
	else:
		return [(r[0],r[1:]) for r in parse(text,select=select)]

## high level interface ##################################

def tab_meta_rows(text='',path='',file=None):
	if path:
		file = open(path,'r')
	if file:
		text = file.read()
	for tab,hint,body in sections(text):
		meta = get_dict(body)
		rows = list(get_rows(body))
		yield tab,meta,rows

def get_rows(text):
	"""yields rows from section body
	
	each row looks like a list of strings but allows access
	to its elements by name and to the column metadata:
	
		for row in get_rows(text):
			x = row[0]
			x = row.column_x
			xt = row.column_x.type
			xt = row[0].type
			xn = row[0].name
	"""
	meta = get_meta(text,select='+',strip=True)
	col_cnt = max([len(m[1]) for m in meta])
	
	for row_as_list in parse(text,col_cnt):
		row = list_obj()
		for i,v in enumerate(row_as_list):
			val = str_obj(v)
			for k,meta_list in meta:
				m = meta_list[i] if i<len(meta_list) else ''
				val.__dict__[k] = m
				if k=='name' and m:
					row.__dict__[m] = val
			row += [val]
		yield row

# @key vs @@key
def get_dict(text,select='@'):
	meta = get_meta(text,select=select,strip=True)
	return dict([(k,v[0]) for k,v in meta])

class list_obj(list): pass
class str_obj(str): pass

###################################################


if __name__=="__main__":
	test = """
	*** sekcja ***
	@k1	va
	@k2	vb
	+type	a	a	b	b
	+name	c1	c2	c3	c4
		to	jest	test:1	abc:2
		aaa	bbb	ccc:3	ddd:4

	*** costam *** xxx
	@k1	v1
	@k2	v2
	+name	col1	col2	col3
		a	b	c
		x	y	z
	"""
	for tab,meta,rows in tab_meta_rows(test):
		print(tab,meta,rows)

