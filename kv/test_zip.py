with open('col.txt','w') as f:
	for x in range(1000000):
		f.write(str(x%2)+',')
