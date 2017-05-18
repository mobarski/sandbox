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

###

def clone_file(f):
	import os
	return os.fdopen(os.dup(f.fileno()))

def line_gen(f,partition):
	f=clone_file(f)
	p_start,p_end = partition
	f.seek(p_start)
	while f.tell()<p_end:
		yield f.readline().rstrip('\r\n')

def raw_gen(f,partition,block_size=None):
	f=clone_file(f)
	block_size = block_size or 4096*16
	p_start,p_end = partition
	f.seek(p_start)
	while f.tell()<p_end:
		cnt = min(block_size, p_end-f.tell())
		yield f.read(cnt)

###

import shlex
import subprocess
def run(f,cnt,cmd,out_prefix,out_suffix='',block_size=None):
	generators = []
	processes = []
	
	### INIT ###
	parts = partitions(f,cnt)
	for i in range(cnt):
		p = parts[i]
		f_out = open('{0}.out.part{1}{2}'.format(out_prefix,i,out_suffix),'w') 
		f_log = open('{0}.log.part{1}{2}'.format(out_prefix,i,out_suffix),'w')
		gen = raw_gen(f,p,block_size)
		generators += [gen]
		args = shlex.split(cmd)
		proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=f_out, stderr=f_log)
		processes += [proc]
		print("[START] partition{0} pid={1} start:{2} stop:{3}".format(i, proc.pid, p[0], p[1]))
		
	### MAIN LOOP ### 
	while generators:
		done = set()
		for gen,proc in zip(generators,processes):
			try:
				block = next(gen)
			except StopIteration:
				done.add((gen,proc))
				continue
			proc.stdin.write(block.encode())
			# print('[ACTIVE] pid={0}'.format(proc.pid))
		for gen,proc in done:
			print("[DONE] pid={0}".format(proc.pid))
			generators.remove(gen)
			processes.remove(proc)
			proc.stdin.close()
			proc.wait()

######################################################################################

if __name__=="__main__":
	f=open('test.txt','r')
	parts = partitions(f,4)
	#print(parts)
	for ps,pe in parts:
		if 0:
			f.seek(ps)
			while f.tell()<pe:
				line = f.readline().rstrip('\r\n')
				print(line)
			print('-'*40)
		if 0:
			gen = line_gen(f,(ps,pe))
			for line in gen:
				print(line)
			print('+'*40)
		if 0:
			gen = raw_gen(f,(ps,pe),10)
			for raw in gen:
				print(raw)
			print('+'*40)
	if 1:
		run(open('test.txt','r'),4,'''python -c "import sys; print(sys.stdin.read())" ''','test','.txt',10)
	

