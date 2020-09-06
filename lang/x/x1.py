from lark import Lark

# https://github.com/lark-parser/lark/blob/master/examples/advanced/python3.lark

# ---[ GRAMMAR ]----------------------------------------------------------------

# TODO pozwolic na a:foo:bar zamiast a:foo():bar() ???

gram = '''
start: stmt+
?stmt: init | assign | augment | call | pipe | block | if | for | for_range | for_in2 | block | break
?expr: atom | infix | cast | call | array | cmp | pipe | attr
init: left ":=" expr
assign: left "=" expr
augment: left AUGMENT expr
?number: dec_num | hex_num
?atom: number | name
left: array | name
type: TYPE | TYPENAME
cast: type "(" expr ")"
call: name "(" args* ")"
args: expr ("," expr)*
infix: expr OP expr
array: name ("[" (expr | slice) "]")+
cmp: expr CMP expr
pipe: expr (":" call)+
attr: expr "." name
slice: range
     | (expr "..") -> slice_from
	 | (".." expr) -> slice_to
?range: expr ".." expr
block: "{" stmt* "}"
if: "if" cmp block elif* else?
elif: "elif" cmp block
else: "else" block
for: "for" block
for_range: "for" name "in" range block
for_in2: "for" name "," name "in" expr block
break: BREAK

name: NAME
dec_num: DEC_NUM
hex_num: HEX_NUM

BREAK: ("continue" | "break")
NAME: /[a-z_][a-zA-Z_0-9]*/
TYPENAME: /[A-Z_][a-zA-Z_0-9]*/
DEC_NUM: /0|[1-9][0-9_]*/i
HEX_NUM: /0x[0-9_a-f]*/i
AUGMENT: ("+=" | "-=" | "*=" | "/=" | "%=" | "&=" | "|=" | "^=" | "<<=" | ">>=")
CMP: ("==" | "!=" | "<" | ">" | "<=" | ">=")
OP: ("+" | "-" | "*" | "/" | "%" | "&" | "|" | "^" | "<<" | ">>")
TYPE: ("i8"|"i16"|"i32"|"i64"|"u8"|"u16"|"u32"|"u64"|"f16"|"f32"|"f64"|"size_t"|"bool"|"int"|"uint")

%import common.WS
%ignore WS
'''

# ---[ TEST ]-------------------------------------------------------------------

code = '''
	a := 4
	for i in 2..10 {
		a += int8(i)
	}
	for i,x in arr[2..5] {
		print(i,x)
	}
	print(a)
'''

# ---[ CODE GENERATOR ]---------------------------------------------------------

p = Lark(gram)
tree = p.parse(code)
#print(tree.pretty())
for x in tree.iter_subtrees():
	c = x.children
	if x.data=='dec_num':
		v = c[0].replace('_','')
		x.code = str(v)
	elif x.data=='infix':
		v = str(c[1])
		x.code = f"{c[0].code} {v} {c[2].code}"
	elif x.data=='name':
		x.code = str(c[0])
	elif x.data=='left':
		x.code = c[0].code
	elif x.data=='assign':
		x.code = f"{c[0].code} = {c[1].code}"
	elif x.data=='init':
		x.code = f"int {c[0].code} = {c[1].code}" # TODO
	elif x.data=='augment':
		x.code = f"{c[0].code} {str(c[1])} {c[2].code}"
	elif x.data=='block':
		code = '; '.join([a.code for a in c])
		x.code = "{ "+code+" }"
	elif x.data=='cast':
		x.code = f"{c[0].code}({c[1].code})"
	elif x.data=='attr':
		x.code = f"{c[0].code}.{c[1].code}"
	# arrays
	elif x.data=='array':
		if c[1].data=='slice':
			a = c[0].code
			a_slice = a+"_slice" # TODO not name
			lo = c[1].code_lo
			hi = c[1].code_hi
			x.code_before = f"Slice {a_slice} = {{ {a}.data, 4, {lo}, {hi} }}\n"
			x.code = f"{a_slice}"
		else:
			x.code_before = ''
			x.code = f"{c[0].code}[{c[1].code}]"
	elif x.data=='slice':
		x.code_lo = f"{c[0].code_lo}"
		x.code_hi = f"{c[0].code_hi}"
		x.code = ""
	# cmp, if, elif, else
	elif x.data=='cmp':
		v = str(c[1])
		x.code = f"({c[0].code} {v} {c[2].code})"	
	elif x.data=='elif':
		x.code = f"else if {c[0].code} {c[1].code}"
	elif x.data=='else':
		x.code = f"else {c[0].code}"
	elif x.data=='if':
		x.code = f'if {c[0].code} '+'\n'.join([a.code for a in c[1:]])
	# call, pipe, args
	elif x.data=='args':
		x.code = ','.join([a.code for a in c])
	elif x.data=='call':
		if len(c)>1:
			x.code = f"{c[0].code}({c[1].code})"
		else:
			x.code = f"{c[0].code}()"
	elif x.data=='pipe':
		obj = c[0].code
		code = obj
		for a in c[1:]:
			fun = a.children[0].children[0].value
			args = a.children[1].code
			code = f"{fun}({code},{args})"
		x.code = code
	# for, break, range
	elif x.data=='range':
		x.code_lo = c[0].code
		x.code_hi = c[1].code
	elif x.data=='for':
		x.code = f"for (;;) {c[0].code}"
	elif x.data=='for_range':
		v = c[0].code
		lo = c[1].code_lo
		hi = c[1].code_hi
		x.code = f"for (int {v}={lo};{v}<{hi};{v}++) {c[2].code}"
	elif x.data=='for_in2':
		v = c[0].code
		v2 = c[1].code
		a = c[2].code
		lo = 0
		hi = f"{a}.len"
		x.code = c[2].code_before + f"for (int {v}={lo};{v}<{hi};{v}++) {c[3].code}"
	elif x.data=='break':
		x.code = str(c[0])
	# ---
	elif x.data=='start':
		print('// START')
		for a in c:
			print(a.code)
		print('// END')
	else:
		x.code = f"TODO {x.data}"
		print(x)

TODO = """

v--- gramatyka
 v-- generator
++ wyrazenia
++ przypisanie (+augment)
+ inicjalizacja
++ typy
++ rzutowanie
++ wywolanie funkcji
++ tablice 
++ porównywanie (< > <= >= == !=)
++ pipe
++ atrybuty
+ plastry (slice)
++ bloki
++ if
++ elif
++ else
++ for {}
++ break, continue
++ for x in 0..10 {}
- for i,x in arr {}
- for x in arr {}
- for x in arr[1..5] {}
- for i=0;i<10;i++ {}
- referencja/dereferencja
- nawiasy
- case / match
- string ' ''' " ""...
-
- inicjalizacja structa
- inicjalizacja tablicy
- definicja structa
- definicja funkcji
- :map
- :filter
- kolejnosc operatorow
- assert
- string interpolation
- // comments
- /* comments

typy:
i8 i16 i32 i64
u8 u16 u32 u64
f32 f64 f16?
bool
size_t
int uint

fn foo(a int, b int) int {
	
}

a := [1,2,3,4]
b := a:map(it*2):filter(it>9):sin():add(2)

for {}
for i<10 {}

[1,2,3,4]:reduce(agg+it,0) == 10
x:sin()
 :add(2)

"""
