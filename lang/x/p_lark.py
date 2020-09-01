from lark import Lark

# https://github.com/lark-parser/lark/blob/master/examples/advanced/python3.lark

gram = '''
start: stmt+
stmt: init | assign | augment | call
expr: atom | infix | cast | call
init: left ":=" expr
assign: left "=" expr
augment: left AUGMENT expr
number: dec_num | hex_num
atom: number | name
left: name
type: TYPE | TYPENAME
cast: type "(" expr ")"
call: name "(" expr ")"
infix: expr OP expr

name: NAME
dec_num: DEC_NUM
hex_num: HEX_NUM

NAME: /[a-z_][a-zA-Z_0-9]*/
TYPENAME: /[A-Z_][a-zA-Z_0-9]*/
DEC_NUM: /0|[1-9][0-9_]*/i
HEX_NUM: /0x[0-9_a-f]*/i
AUGMENT: ("+=" | "-=" | "*=" | "/=" | "%=" | "&=" | "|=" | "^=" | "<<=" | ">>=")
OP: ("+" | "-" | "*" | "/" | "%" | "&" | "|" | "^" | "<<" | ">>")
TYPE: ("i8"|"i16"|"i32"|"i64"|"u8"|"u16"|"u32"|"u64"|"f16"|"f32"|"f64"|"size_t"|"bool"|"int"|"uint")

%import common.WS
%ignore WS
'''

code = '''
	x := 1_000
	y = x + i16(2)
	z = x + sin(y) + 3
'''

p = Lark(gram)
tree = p.parse(code)
print(tree.pretty())

TODO = """
+ wyrazenia
+ przypisanie (+augment)
+ inicjalizacja
+ typy
+ rzutowanie
- wywolanie funkcji
- for
- break, continue
- bloki
- tablice 
- porównywanie (< > <= >= == !=)
- if
- referencja/dereferencja
- :map
- :filter
- kolejnosc operatorow
-
- atrybuty
- metody/pipe
- plastry (slice)
- deklatacja funkcji
- struct



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
b := a:map(it*2):filter(it>9)

for {}
for i<10 {}


"""