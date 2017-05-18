from __future__ import print_function

###

def partitions(f,cnt):
	"return list of file partitions as (part_start,part_end) file offsets"
	out = []
	initial_pos = f.tell()
	f.seek(0,2) # seek end
	f_size = f.tell()
	avg_part_size = f_size/cnt
	f.seek(0) # seek start
	prev = 0
	for n in range(cnt-1):
		target_part_end = int((n+1)*avg_part_size)
		f.seek(min(f_size,target_part_end))
		f.readline()
		pos = f.tell()
		out += [(prev,pos)]
		prev=pos
	out += [(prev,f_size)]
	f.seek(initial_pos)
	return out

###

def clone_file(f):
	return open(f.name,f.mode)

def line_gen(f,partition):
	f=clone_file(f)
	p_start,p_end = partition
	f.seek(p_start)
	while f.tell()<p_end:
		line = f.readline().rstrip('\r\n')
		yield line

def raw_gen(f,partition,block_size):
	f=clone_file(f)
	p_start,p_end = partition
	f.seek(p_start)
	while f.tell()<p_end:
		cnt = min(block_size, p_end-f.tell())
		raw = f.read(cnt)
		yield raw

###

import shlex
import subprocess
import time
def run(cmd,f,cnt,out_prefix,out_suffix='',block_size=4096):
	"run CMD in parallel batch on CNT partitions of line oriented file F"
	t0=time.time()
	generators = []
	processes = []
	meta_by_pid = {}
	
	### INIT ###
	f = open(f,'rb') if isinstance(f,str) else f
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
		### DIAGNOSTICS ###
		print("[START]\tpartition={0} pid={1} todo={4} start={2} stop={3}".format(i, proc.pid, p[0], p[1],p[1]-p[0]))
		pid = proc.pid
		meta_by_pid[pid] = {}
		meta_by_pid[pid]['partition']=i
		meta_by_pid[pid]['part_start']=p[0]
		meta_by_pid[pid]['part_end']=p[1]
		meta_by_pid[pid]['todo_bytes']=p[1]-p[0]
		meta_by_pid[pid]['done_bytes']=0
		meta_by_pid[pid]['start_time']=time.time()
		
	### MAIN LOOP ### 
	while generators:
		done = set()
		for gen,proc in zip(generators,processes):
			try:
				block = next(gen)
			except StopIteration:
				done.add((gen,proc))
				continue
			proc.stdin.write(block)
			meta_by_pid[proc.pid]['done_bytes'] += len(block)
			# print('[ACTIVE] pid={0}'.format(proc.pid))
		for gen,proc in done:
			pid = proc.pid
			m = meta_by_pid[pid]
			print("[DONE]\tpartition={2} pid={0} done={1} time={3:.2f}s".format(pid,m['done_bytes'],m['partition'],time.time()-m['start_time']))
			generators.remove(gen)
			processes.remove(proc)
			proc.stdin.close()
			proc.wait()
	
	### END STATISITCS ###
	print('[END]\ttime={0:.2f}s'.format(time.time()-t0))


def run_str(cmd,f,cnt,out_prefix,out_suffix='',block_size=4096):
	"run CMD in parallel streaming on CNT partitions of line oriented input F"
	t0=time.time()
	processes = []
	meta_by_pid = {}
	
	### INIT ###
	f = open(f,'rb') if isinstance(f,str) else f
	for i in range(cnt):
		f_out = open('{0}.out.part{1}{2}'.format(out_prefix,i,out_suffix),'w') 
		f_log = open('{0}.log.part{1}{2}'.format(out_prefix,i,out_suffix),'w')
		args = shlex.split(cmd)
		proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=f_out, stderr=f_log)
		processes += [proc]
		### DIAGNOSTICS ###
		print("[START]\tpartition={0} pid={1} block_size={2}".format(i, proc.pid, block_size))
		pid = proc.pid
		meta_by_pid[pid] = {}
		meta_by_pid[pid]['partition']=i
		meta_by_pid[pid]['done_bytes']=0
		meta_by_pid[pid]['start_time']=time.time()
		
	### MAIN LOOP ### 
	while processes:
		done = set()
		for proc in processes:
			block = f.read(block_size)+f.readline()
			if len(block)<block_size:
				done.add(proc)
			proc.stdin.write(block)
			meta_by_pid[proc.pid]['done_bytes'] += len(block)
			# print('[ACTIVE] pid={0}'.format(proc.pid))
		for proc in done:
			pid = proc.pid
			m = meta_by_pid[pid]
			print("[DONE]\tpartition={2} pid={0} done={1} time={3:.2f}s".format(pid,m['done_bytes'],m['partition'],time.time()-m['start_time']))
			processes.remove(proc)
			proc.stdin.close()
			proc.wait()
	
	### END STATISITCS ###
	print('[END]\ttime={0:.2f}s'.format(time.time()-t0))

######################################################################################

if __name__=="__main__":
	run_str('python -c "import sys; print(sys.stdin.read())" ', 'test.txt', 4, 'test/test', '.txt', 5)
	

