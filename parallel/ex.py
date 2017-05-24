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

	def split(self, *a,**kw): return self._add_op('split',a,kw)
	def pipe(self, *a, **kw): return self._add_op('pipe',a,kw)
	def join(self,*a,**kw): return self._add_op('join',a,kw)

	def run(self):
		n = 1
		dag = {}
		for step,(op,a,kw) in enumerate(self.ops):
			dag[step] = {}
			if op=='join':
				n=1
			for part in range(n):
				dag[step][part] = dict(op=op,a=a,kw=kw)
			if op=='split': # one per job -> python loop
				n=a[0]
		from pprint import pprint
		pprint(dag)

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

(Job()
	.pipe('cat plik.txt')
	.split(4)
	.pipe('parse.py')
	.pipe('sort')
	.join()
	.pipe('hadoop fs -put plik.txt')
).run()

