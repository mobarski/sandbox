def partitions(f,cnt):
	"return list of file partitions as (part_start,part_end) file offsets"
	out = []
	initial_pos = f.tell()
	f.seek(0,2) # seek end
	fsize = f.tell()
	psize = int(fsize/cnt)
	f.seek(0) # seek start
	prev = 0
	for n in range(cnt-1):
		f.seek(prev+psize,0)
		f.readline()
		pos = f.tell()
		out += [(prev,pos)]
		prev=pos
	out += [(prev,fsize)]
	f.seek(initial_pos)
	return out

import os
def line_gen(f,partition):
	#f=os.fdopen(os.dup(f.fileno()))
	p_start,p_end = partition
	f.seek(p_start)
	while f.tell()<p_end:
		yield f.readline().rstrip('\r\n')

if __name__=="__main__":
	f=open('test.txt','r')
	parts = partitions(f,4)
	print(parts)
	for ps,pe in parts:
		if 0:
			f.seek(ps)
			while f.tell()<pe:
				line = f.readline().rstrip('\r\n')
				print(line)
			print('-'*40)
		if 1:
			gen = line_gen(f,(ps,pe))
			for line in gen:
				print(line)
			print('+'*40)
