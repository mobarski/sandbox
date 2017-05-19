## p7.py - parallel processing microframework
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: MK2 MOD0

from __future__ import print_function

# TODO - fix python2 error in stdin.write(block) for some input files
# TODO - refactor all run functions

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
def run_batch(cmd,f,cnt,out_prefix,out_suffix='',block_size=4096):
	"run CMD in parallel batch on CNT partitions of line oriented file F using single data pump"
	t0=time.time()
	generators = []
	processes = []
	meta_by_pid = {}
	
	### INIT ###
	print('[BEGIN]\tpartitions={0} block_size={1}'.format(cnt,block_size))
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
	while processes:
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
	print('[END]\ttime={0:.2f}s partitions={1} block_size={2}'.format(time.time()-t0,cnt,block_size))


def run_stream(cmd,f,cnt,out_prefix,out_suffix='',block_size=4096):
	"run CMD in parallel streaming on CNT partitions of line oriented input F"
	t0=time.time()
	processes = []
	meta_by_pid = {}
	
	### INIT ###
	print('[BEGIN]\tpartitions={0} block_size={1}'.format(cnt,block_size))
	f = open(f,'rb') if isinstance(f,str) else f
	for i in range(cnt):
		f_out = open('{0}.out.part{1}{2}'.format(out_prefix,i,out_suffix),'w') 
		f_log = open('{0}.log.part{1}{2}'.format(out_prefix,i,out_suffix),'w')
		args = shlex.split(cmd)
		proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=f_out, stderr=f_log)
		processes += [proc]
		### DIAGNOSTICS ###
		print("[START]\tpartition={0} pid={1}".format(i, proc.pid))
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
	print('[END]\ttime={0:.2f}s partitions={1} block_size={2}'.format(time.time()-t0,cnt,block_size))

import os
def run_part(cmd,f,part_num,part_start,part_stop,out_prefix,out_suffix='',block_size=4096):
	i = part_num
	f = open(f,'rb') if isinstance(f,str) else f
	f_out = open('{0}.out.part{1}{2}'.format(out_prefix,i,out_suffix),'w') 
	f_log = open('{0}.log.part{1}{2}'.format(out_prefix,i,out_suffix),'w')
	p = (part_start,part_stop)
	gen = raw_gen(f,p,block_size)
	args = shlex.split(cmd)
	proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=f_out, stderr=f_log)
	pid = proc.pid
	print("[START]\tpartition={0} pid={2} pid_pump={1} todo={5} start={3} stop={4}".format(i,os.getpid(),pid,part_start,part_stop,part_stop-part_start))
	sys.stdout.flush()
	start_time=time.time()
	done_bytes=0
	
	### MAIN LOOP ###
	while True:
		try:
			block = next(gen)
		except StopIteration:
			proc.stdin.close()
			break
		proc.stdin.write(block)
		done_bytes += len(block)
	print("[DONE]\tpartition={0} pid={2} pid_pump={1} done={3} time={4:.2f}s".format(i,os.getpid(),pid,done_bytes,time.time()-start_time))

import sys
def run_batch2(cmd,f,cnt,out_prefix,out_suffix='',block_size=4096):
	"run CMD in parallel batch on CNT partitions of line oriented file F using multiple data pumps"
	t0=time.time()
	print('[BEGIN]\tpartitions={0} block_size={1}'.format(cnt,block_size))
	processes = []
	f_name = f if isinstance(f,str) else f.name
	f = open(f,'rb') if isinstance(f,str) else f
	parts = partitions(f,cnt)
	for i in range(cnt):
		p = parts[i]
		args = shlex.split('python p7.py')
		proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=sys.stdout)
		args_str = str([cmd,f_name,i,p[0],p[1],out_prefix,out_suffix,block_size])
		proc.stdin.write(args_str.encode())
		proc.stdin.close()
		processes += [proc]	
	for p in processes:
		p.wait()

	### END STATISITCS ###
	print('[END]\ttime={0:.2f}s partitions={1} block_size={2}'.format(time.time()-t0,cnt,block_size))

def run_part_main():
	args_str = sys.stdin.read()
	args = eval(args_str)
	run_part(*args)

######################################################################################

run = run_stream # default run function

if __name__=="__main__":
	run_part_main()
