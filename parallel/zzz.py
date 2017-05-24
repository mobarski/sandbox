## p7.py - parallel processing microframework
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: mk3 mod1 (XJob->BatchJob,small refactoring)

# TODO - list of input files
# TODO - reducer
# TODO - combiner
# TODO - split output into multiple streams (within partition)

###  py2 vs py3 compatibility ##################################

from __future__ import print_function
try:
	BrokenPipe = BrokenPipeError
except:
	BrokenPipe = IOError

### UTILS ######################################################
@asdasd
def list_partitions(f,cnt):
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
	f.seekf.readline().rstrip('\r\n')
		yield line

def raw_gen(f,partition,block_size):
	f=clone_file(f)
	p_start,p_end = partition
	f.seek(p_start)
	while f.tell()<p_end:z
		cnt = min(block_size, p_end-f.tell())
		raw = f.read(cnt)
		yield raw

class xdict(dict):
	def __getattr__(self,x):
		return self[x]
	def __setattr__(self,k,v):
		self[k]=v

### PUMP ####################################################################

def run_pump(f, start_offset, end_offset, block_size=4096):
	f=open(f,'rb') if isinstance(f,str) else f
	sys.stdout = os.fdopen(sys.stdout.fileno(),'wb')
	if sys.platform == "win32" and sys.version_info.major==2:
		import msvcrt
		msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
	gen = raw_gen(f,(start_offset,end_offset),block_size)
	for data in gen:
		sys.stdout.write(data)

def run_pump_main():
	args_str = sys.stdin.read()
	args = eval(args_str)
	##sys.stderr.write(str(args)+'\n')
	run_pump(*args)

### RUN FUNCTIONS #############################################################

import shlex
import subprocess
import time
import sys
import os

class Job:
	"""run CMD in parallel on local computer using CNT subprocesses, piping data from file F in streaming mode
	
	Arguments:
	* cmd - command to be run in pralallel, it should read from standard input and write to standard output and standard error
	* f - input filename or IO object
	* cnt - number of partitions / subprocesses
	* out - output filename or IO object, if contains {0} then output will be separated for each partition
	* log - log filename or IO object, if contains {0} then logs will be separated for each partition
	* block_size - approximate size (in bytes) of block of data for reading/writting
	"""
	def __init__(self,cmd,f,cnt,out=None,log=None,block_size=4096):
		self.cmd=cmd
		self.f=open(f,'rb') if isinstance(f,str) else f
		self.f_name = self.f.name
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
			done = self.pump_data()

			for i in done:
				self.end_proc(i)
				m = self.meta[i]
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

	def pump_data(self):
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
		return done

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
			m['pipe_in'] = subprocess.PIPE
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

	def end_proc(self,i):
		m = self.meta[i]
		m.proc.stdin.close()
		m.proc.wait()

	def pipe_out(self,i):
		return open(self.out.format(i),'wb') if isinstance(self.out,str) else self.out 
	
	def pipe_log(self,i):
		return open(self.log.format(i),'wb') if isinstance(self.log,str) else self.log 

######################################################################################

class BatchJob(Job):		
	def init_pipes(self):
		Job.init_pipes(self)
		pump_cmd = "python p7ex3.py pump"
		pump_args = shlex.split(pump_cmd)
		partitions = list_partitions(self.f, self.cnt)
		for i in range(self.cnt):
			m=self.meta[i]
			p_start,p_end = partitions[i]
			pump = subprocess.Popen(pump_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=m.pipe_log)
			pump_param = [self.f_name, p_start, p_end, self.block_size]
			pump.stdin.write(str(pump_param).encode())
			pump.stdin.close()
			m['pump'] = pump
			m['pump_pid'] = pump.pid
			m['pipe_in'] = pump.stdout
			m['done'] = 'N/A'

	def pump_data(self):
		done = set()
		for i in self.active:
			m = self.meta[i]
			rc = m.pump.poll()
			if rc != None:
				m.pump.wait()
				m['pump_rc']=rc
				done.add(i)
		if not done: time.sleep(0.01)
		return done

	def partition_start_stats(self,i):
		m = self.meta[i]
		print('[START]\tpartition={0} pid={1} pump_pid={2}'.format(
			i,m.pid,m.pump_pid))

	def partition_done_stats(self,i):
		m = self.meta[i]
		print("[DONE]\tpartition={2} pid={0} pump_pid={1} time={3:.2f}s".format(
			m.pid,m.pump_pid,m.part,m.time))

	def end_proc(self,i):
		m = self.meta[i]
		m.proc.wait()

#################################################################################

if __name__=="__main__":
	if 'pump' not in sys.argv: exit()
	run_pump_main()
