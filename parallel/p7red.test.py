from __future__ import print_function
import sys

lines = sys.stdin.readlines()
rows = [str.partition(x,' ') for x in lines if x.strip()]

out_kv = {}
for k,_,x in rows:
	out_kv[k] = out_kv.get(k,0) + int(x)

for k,v in sorted(out_kv.items()):
	print(k,v)
