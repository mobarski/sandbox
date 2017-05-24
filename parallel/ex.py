import shlex
import subprocess
import time
import sys
import os

class Job:
	def __init__(self,hint=''):
		self.hint=hint
		self.ops = []
	def _add_op(self,op,a,kw):
		self.ops += [(op,a,kw)]
		return self

	def pipe(self, *a, **kw): return self._add_op('pipe',a,kw)
	def map(self,  *a, **kw): return self._add_op('map',a,kw)

	def run(self):
		for op,a,kw in self.ops:
			print('TODO RUN',op,a,kw)

def pump(fi,fo,fe,block_size):
	block = fi.read(block_size)+fi.readline()
	while True:
		if len(block)<block_size: break
		fo.write(block)
