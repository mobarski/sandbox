## DECLARATIVE AUTOMATION SHELL
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: MK7 MOD1

#################################################

import re
from textwrap import dedent
from collections import defaultdict

p_section = """ (?xms)
	^ \*{3} \s* (.+?) \s* \*{3}	# name
	[ \t]* (.*?) [ \t]* $		# meta
	(.+?) (?= ^ \*{3} | \Z)	# body
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
		lines = [x.rstrip() for x in re.split(p_eol,text) if x.strip() and x[0] in ('\t','|')] # 

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
			if '@' in row: # line extension support
				extension = []
				while True: # get extension lines
					if not lines: continue
					ext = fields(lines[0])
					if ext[0] != '|': break
					lines.pop(0)
					extension += [ext]
				for i,col in enumerate(row): # build columns 
					if col != '@': continue
					row[i] = ' '.join([x[i+1] for x in extension if len(x)>=i+1 and x[i+1]]) # TODO DECISION - strip
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

def split(text='',path='',file=None):
	if path:
		file = open(path,'r')
	if file:
		text = file.read()
	for tab,hint,body in sections(text):
		meta = get_dict(body)
		rows = list(get_rows(body))
		if rows:
			setattr(rows[0],'first',True)
			setattr(rows[-1],'last',True)
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
	meta = get_meta(text,select='>',strip=True)
	col_cnt = max([len(m[1]) for m in meta]) if meta else 0
	
	for row_as_list in parse(text,col_cnt):
		row = list_obj()
		for i,v in enumerate(row_as_list):
			setattr(row,'first',False) # real value set in tab_meta_rows
			setattr(row,'last',False) # real value set in tab_meta_rows
			val = str_obj(v)
			for k,meta_list in meta:
				m = meta_list[i] if i<len(meta_list) else ''
				setattr(val,k,m)
				if k=='name' and m:
					setattr(row, m.replace(' ','_').lower(), val)
			row += [val]
		yield row

def get_dict(text,select='@'):
	meta = get_meta(text,select=select,strip=True)
	out = defaultdict(list)
	for k,v in meta:
		out[k].append(v[0])
	return dict_obj([(k,v[0] if len(v)==1 else v) for k,v in out.items()])

## UTIL ##############################################

class dict_obj(dict):
	def __getattr__(self,x):
		return self.get(x,'')
class attr_default_str:
	def __getattr__(self,x):
		return self.__dict__.get(x,'')
class list_obj(list,attr_default_str): pass
class str_obj(str,attr_default_str): pass

###################################################

if __name__=="__main__":
	test = """
	*** sekcja ***
	>name	c1	c2	c3	c4
		@	jest	@	abc
	|			x
	|	b		y
	|	c		z
		aaa	bbb	ccc	ddd
	"""
	tab,meta,rows = next(split(test))
	print(tab,meta,rows)
	for row in rows:
		pass
