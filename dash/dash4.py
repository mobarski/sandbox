## DECLARATIVE AUTOMATION SHELL
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: EX4 MOD1

## MOD1 CHANGE:
## - fixed cnt argument
## EX4 CHANGES:
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

def parse(text,cnt=0,default='',empty='.',select='',strip=True):
	"parse body of dash section and return list of values for each row"
	def field(x):
		x = x.strip() if strip else x
		return x if x!=empty else default
		
	def fields(line):
		if cnt:
			return ([field(x) for x in re.split(p_sep,line)]+[default]*cnt)
		else:
			return [field(x) for x in re.split(p_sep,line)]

	if select:
		lines = [x.rstrip() for x in re.split(p_eol,text) if x.strip() and x[0] in select]
	else:
		lines = [x.rstrip() for x in re.split(p_eol,text) if x.strip() and x[0]=='\t']

	out = []
	while lines:
		line = lines.pop(0)
		row = fields(line)
		if select:
			if cnt:
				row = row[:cnt]
		else:
			row = row[1:] # skip first column
			if cnt:
				row = row[:cnt]
		out += [row]
		# TODO support of line extension
			#~ if '@' in row: # line extension support
				#~ extension = []
				#~ while True:
					#~ if not lines: break
					#~ ext = fields(lines[0])
					#~ if ext[0] != '|': break
					#~ lines.pop(0)
					#~ extension += [ext]
				#~ n = 1
				#~ for i in range(len(row)):
					#~ if row[i]!='@': continue
					#~ row[i] = ' '.join([x[n] for x in extension if len(x)>=n+1])
					#~ n += 1
	return out

def sections(text):
	"return [name,hint,body] for each section"
	return re.findall(p_section,dedent(text))


###################################################


if __name__=="__main__":
	test = """
	*** sekcja ***
		to	jest	test	:)
		aaa	bbb	ccc	ddd

	*** costam *** xxx
	@k1	v1
	@k2	v2
	>	col1	col2	col3
		a	b	c
	"""
	for name,hint,body in sections(test):
		print(name,parse(body))
		print(name,parse(body,select='@'))

