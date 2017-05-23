## p7.py - parallel processing microframework
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: EX3 MOD1 (working Job class)

# TODO - p7.py just as a pump to stdout, piping in run function
# TODO - list of input files
# TODO - reducer
# TODO - combiner

###  py2 vs py3 compatibility ##########################################

from __future__ import print_function
try:
	BrokenPipe = BrokenPipeError
except:
	BrokenPipe = IOError

### UTILS ######################################################

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

class xdict(dict):
	def __getattr__(self,x):
		return self[x]
	def __setattr__(self,k,v):
		self[k]=v

### RUN FUNCTIONS #############################################################

import shlex
import subprocess
import time
import sys
import os

class Job:
	def __init__(self,cmd,f,cnt,out=None,log=None,block_size=4096):
		self.cmd=cmd
		self.f=open(f,'rb') if isinstance(f,str) else f
		self.cnt=cnt
		self.out=open(out,'wb') if isinstance(out,str) and '{0}' not in out else out or sys.stdout
		self.log=open(log,'wb') if isinstance(log,str) and '{0}' not in log else log or sys.stderr
		self.block_size=block_size
		self.meta = {}
		self.args = shlex.split(cmd)
		self.active = set()

	def run(self):
		self.t0=time.time()
		self.begin_stats()
		self.init()
		while self.active:
			done = set()
			
			for i in self.active:
				m = self.meta[i]
				block = self.f.read(self.block_size)+self.f.readline()
				if len(block)<self.block_size:
					done.add(i)
				try:
					m.proc.stdin.write(block)
				except BrokenPipe:
					pass # TODO
				else:
					m['done'] += len(block)

			for i in done:
				m = self.meta[i]
				m.proc.stdin.close()
				m.proc.wait()
				m['end_time']=time.time()
				m['time']=time.time()-m.start_time
				self.partition_done_stats(i)
				self.active.remove(i)
		self.end_stats()

	def begin_stats(self):
		print('[BEGIN]\tpartitions={0} block_size={1}'.format(self.cnt, self.block_size))
	
	def partition_start_stats(self,i):
		m = self.meta[i]
		print('[START]\tpartition={0} pid={1}'.format(
			i,m.pid))

	def partition_done_stats(self,i):
		m = self.meta[i]
		print("[DONE]\tpartition={2} pid={0} done={1} time={3:.2f}s".format(
			m.pid,m.done,m.part,m.time))
	
	def end_stats(self):
		print('[END]\ttime={0:.2f}s partitions={1} block_size={2}'.format(time.time()-self.t0, self.cnt, self.block_size))

	def init(self):
		self.init_meta()
		self.init_pipes()
		self.init_proc()

	def init_meta(self):
		for i in range(self.cnt):
			self.meta[i] = xdict()
		
	def init_pipes(self):
		for i in range(self.cnt):
			m=self.meta[i]
			m['part'] = i
			m['pipe_in'] = self.pipe_in(i)
			m['pipe_out'] = self.pipe_out(i)
			m['pipe_log'] = self.pipe_log(i)
	
	def init_proc(self):
		for i in range(self.cnt):
			m=self.meta[i]
			proc = subprocess.Popen(self.args, stdin=m.pipe_in, stdout=m.pipe_out, stderr=m.pipe_log)
			self.active.add(i)
			m['pid'] = proc.pid
			m['proc'] = proc
			m['done'] = 0
			m['start_time']=time.time()
			self.partition_start_stats(i)

	def pipe_in(self,i):
		return subprocess.PIPE
	
	def pipe_out(self,i):
		return open(self.out.format(i),'wb') if isinstance(self.out,str) else self.out 
	
	def pipe_log(self,i):
		return open(self.log.format(i),'wb') if isinstance(self.log,str) else self.log 

### PUMP ###

def run_pump(f, start_offset, end_offset, block_size=4096):
	f=open(f,'rb') if isinstance(f,str) else f
	gen = raw_gen(f,(start_offset,end_offset),block_size)
	for data in gen:
		sys.stdout.write(data)

def run_pump_main():
	args_str = sys.stdin.read()
	args = eval(args_str)
	run_pump(*args)

######################################################################################

if __name__=="__main__":
	#run_pump_main()
	from pprint import pprint
	cmd = 'python -c "import sys; sys.stdout.write(sys.stdin.read())" '
	f_in = "test.txt"
	f_out = 'test/out.part.txt'
	f_log = 'test/log.part.txt'
	job=Job(cmd,f_in,4,f_out,f_log,block_size=5)
	#pprint(job.meta)
	job.run()

