from lark import Lark

# VS V:
# - methods via pipe operator
# - mut only in function api
# - everything is pub

# ---[ GRAMMAR ]---

# TODO: block
# TODO: if / elif / else
# TODO: array constant ie [1,3,5,7]
# TODO: multidim arrays
# TODO: array get
# TODO: array set
# TODO: match
# TODO: if expr
# TODO: pipe
# TODO: member . vs ->
# TODO: struct def
# TODO: function def
# TODO: reference, dereference
# TODO: for {} / break / continue
# TODO: +- number prefix

grammar = '''
start: stmt+
stmt: init | assign | augment | call
?expr: atom | cast | new_array | cmp | call

init: left ":=" expr
assign: left "=" expr
augment: left AUGMENT expr
cmp: expr CMP expr

left: name
cast: type "(" expr ")"
call: name "(" args* ")"
args: expr ("," expr)*
new_array: "[" expr? "]" type "{" "}"
type: TYPE | STRUCTNAME
?atom: number | name | c_str
?number: dec_num | hex_num

name: NAME
dec_num: DEC_NUM
hex_num: HEX_NUM
c_str: C_STR

C_STR: /c"[^"]*"/
NAME: /[a-z_][a-zA-Z_0-9]*/
STRUCTNAME: /[A-Z_][a-zA-Z_0-9]*/
DEC_NUM: /0|[1-9][0-9_]*/i
HEX_NUM: /0x[0-9_a-f]*/i

AUGMENT: ("+=" | "-=" | "*=" | "/=" | "%=" | "&=" | "|=" | "^=" | "<<=" | ">>=")
TYPE: ("i8"|"i16"|"i32"|"i64"|"u8"|"u16"|"u32"|"u64"|"f16"|"f32"|"f64"|"size_t"|"bool"|"int"|"uint")
CMP: ("==" | "!=" | "<" | ">" | "<=" | ">=")

%import common.WS
%ignore WS
'''

# ---[ TEST ]---

code = '''
a := u8(0xA4)
b := 42
c := [8]int{}
b += 13
printf(c"%d",a<b)
'''

# ---[ UTIL ]---

import sys
import os

fo = open('a.c','w')
def output(text):
	print(text,file=sys.stdout)
	print(text,file=fo)
	fo.flush()

# ---[ GENERATOR ]---

includes = '''
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>


#define i8 int8_t
#define i16 int16_t
#define i32 int32_t
#define i64 int64_t

#define u8 uint8_t
#define u16 uint16_t
#define u32 uint32_t
#define u64 uint64_t

#define f32 float
#define f64 double

#define charptr char*
#define voidptr void*

typedef struct {
	voidptr  data;
	i32      item_size;
	i32      len;
	i32      cap;
} array;

'''

p = Lark(grammar)
tree = p.parse(code)
for x in tree.iter_subtrees():
	c = x.children
	if x.data=='start':
		output(includes)
		output('int main() {')
		for a in c:
			output(a.code)
		output('}')
	elif x.data=='stmt':
		x.code='\t'+c[0].code+';'
	#
	elif x.data=='name':
		x.code=c[0]
	elif x.data=='left':
		x.code=c[0].code
	elif x.data=='dec_num':
		x.code=c[0].replace('_','')
		x.type='int'
	elif x.data=='hex_num':
		x.code=c[0].replace('_','')		
		x.type='int'
	elif x.data=="c_str":
		x.code=c[0][1:]
		x.type='charptr'
	elif x.data=='cmp':
		x.code = f"({c[0].code} {c[1]} {c[2].code})"			
	elif x.data=='augment':
		x.code = f"{c[0].code} {str(c[1])} {c[2].code}"
	elif x.data=='init':
		if hasattr(c[1],'array'):
			x.code = f"{c[1].type} {c[0].code}{c[1].array} = {c[1].code}"
		else:
			x.code = f"{c[1].type} {c[0].code} = {c[1].code}"
	elif x.data=='assign':
		# TODO check type
		x.code = f"{c[0].code} = {c[1].code}"
	# TYPE
	elif x.data=='cast':
		x.code=f"(({c[0].code}){c[1].code})"
		x.type=c[0].code
	elif x.data=='type':
		x.code=c[0]
	elif x.data=="new_array":
		x.code='{}'
		x.array='[]' if len(c)==1 else f'[{c[0].code}]'
		x.type=c[-1].code
	# call, pipe, args
	elif x.data=='args':
		x.code = ','.join([a.code for a in c])
	elif x.data=='call':
		if len(c)>1:
			x.code = f"{c[0].code}({c[1].code})"
		else:
			x.code = f"{c[0].code}()"
	# ELSE
	else:
		x.code = f"TODO {x.data}"
		print(x)

# ---[  ]---

fo.close()
os.system('clang a.c')
