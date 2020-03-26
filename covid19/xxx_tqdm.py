from tqdm import tqdm
from time import sleep

def foo():
	sleep(0.2)

data = (i**2 for i in range(200))
for i in tqdm(data,'foo',200):
	foo()
