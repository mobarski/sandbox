class Job:
	def __init__(self,hint=''):
		self.ops = []
	def _add_op(self,op,a,kw):
		self.ops += [(op,a,kw)]
		return self
		
	def input(self,   *a, **kw): return self._add_op('input',a,kw)
	def output(self,  *a, **kw): return self._add_op('output',a,kw)
	def pipe(self,    *a, **kw): return self._add_op('pipe',a,kw)
	def split(self,   *a, **kw): return self._add_op('split',a,kw)
	def map(self,     *a, **kw): return self._add_op('map',a,kw)
	def flat_map(self,*a, **kw): return self._add_op('flat_map',a,kw)
	def reduce(self,  *a, **kw): return self._add_op('reduce',a,kw)
	def combine(self, *a, **kw): return self._add_op('combine',a,kw)

	def run(self):
		for op,a,kw in self.ops:
			print('TODO RUN',op,a,kw)

job =(  Job('opis joba')
	.input(file='test.txt')
	.split(8)
	.pipe()
	.map()
	.reduce()
	.pipe()
	.output()
	)

job.run()

##

import p7
from pprint import pprint
cmd = '''python -c "import sys,os; fi=os.fdopen(0,'rb'); fo=os.fdopen(1,'wb'); fo.write(fi.read())" '''
f_in = "test.txt"
f_out = 'test/out.part.txt'
f_log = 'test/log.part.txt'
##job=p7.BatchJob(cmd,f_in,4,f_out,f_log,block_size=10)
##pprint(job.meta)
job.run()

#~ job =(  Job('opis joba')
	#~ .file_input('test.txt')
	#~ .split(n=4,block_size=10)
	#~ .pipe('''python -c "import sys,os; fi=os.fdopen(0,'rb'); fo=os.fdopen(1,'wb'); fo.write(fi.read())" ''')
	#~ .join()
	#~ .pipe('sort')
	#~ .file_output('out.txt')
	#~ .select(1).file_output('log.txt')
	#~ )

import itertools
def flat_map(f,iter):
	return itertools.chain.from_iterable(map(f,iter))

print(list(flat_map(lambda x:x,[[1],[2],[],[3,4]])))


