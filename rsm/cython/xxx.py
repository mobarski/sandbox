import numpy as np

a = np.random.randint(1,100,(5,8))
print(a)

b = np.random.randint(1,100,22)
print(b)

# P = 5
# for i in range(0,len(b),P):
	# b[i:i+P].sort()
# print(b)

def sort_window(a, width):
	for i in range(0, len(a), width):
		a[i:i+width].sort()

sort_window(b,6)
print(b)
