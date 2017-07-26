from __future__ import print_function
import sys

lines = sys.stdin.readlines()
rows = [str.partition(x,' ') for x in lines if x.strip()]

key_sum = 0
key = rows[0][0]
for k,_,x in rows:
	if k!=key:
		print(key,key_sum)
		key_sum = 0
		key = k
	key_sum += int(x)
print(key,key_sum)
