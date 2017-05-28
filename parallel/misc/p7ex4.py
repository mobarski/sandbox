import shlex
import subprocess
import time
import sys
import os
import multiprocessing as mp

class Job:
	def __init__(self,hint=''):
		self.hint=hint
		self.ops = []
	def _add_op(self,op,a,kw):
		self.ops += [(op,a,kw)]
		return self

	def split(self, *a, **kw): return self._add_op('split',a,kw)
	def pipe(self,  *a, **kw): return self._add_op('pipe',a,kw)
	def join(self,  *a, **kw): return self._add_op('join',a,kw)

	def proc_cnt(self):
		"number of parallel processes in each stage"
		n = 1
		out = []
		for stage,(op,a,kw) in enumerate(self.ops):
			if op=='join':
				n = 1
				out += [n]
			elif op=='split':
				out += [n]
				n *= a[0]
			else:
				out += [n]
		return out

	def pipes1(self):
		cnt = self.proc_cnt()
		cnt[0] = 0
		cnt += [0]
		print(cnt)
		for stage,p,p_next in zip(range(len(cnt)),cnt,cnt[1:]):
			print(self.ops[stage][0])
			#print(stage,self.ops[stage][0],p,p_next)
			print('  create out fifo:')
			for i in range(p_next):
				print('    s{0}p{1}'.format(stage,i))
			print('  create proc:')
			for i in range(p):
				print('    {0} i:s{1}p{2} o:s{3}p{4}'.format(self.ops[stage][0],stage-1,i,stage,i))
			
	def pipes(self):
		stage_cnt = len(self.ops)
		proc_cnt = self.proc_cnt()
		for s in reversed(range(stage_cnt)):
			p_cnt = proc_cnt[s]
			print('stage',s,self.ops[s][0])
			for p in range(p_cnt):
				if s==stage_cnt-1:
					q=0
				elif proc_cnt[s+1]==p_cnt:
					q=p
				elif proc_cnt[s+1]>p_cnt:
					q=list(range(proc_cnt[s+1]))
				else:
					q=0					
				print(' s{0}p{1} i={2}:{3} o={4}:{5}'.format(s,p,s,p,s+1,q))
			print()
		

#~ def pump(fi,fo,fe,cfg):
	#~ block_size = cfg.get('block_size',4096)
	#~ block = fi.read(block_size)+fi.readline()
	#~ while True:
		#~ if len(block)<block_size: break
		#~ fo.write(block)

#~ def pipe(fi,fo,fe,cfg):
	#~ cmd = cfg['cmd']
	#~ cmd_args = shlex.parse(cmd)
	#~ proc = subprocess.Popen(cmd_args)

job=(Job()
	.pipe('cat plik.txt')
	.split(2)
	.pipe('cat')
	#.split(2)
	.pipe('cat')
	.pipe('sort')
	.join()
	.pipe('hadoop fs -put plik.txt')
).pipes()


