import shlex
import time
import sys
import os
import multiprocessing as mproc
import subprocess as sproc
from pprint import pprint

# IMPORTANT - writes to pipes are atomic if len(data)<=pipe_buf (4096 for linux)
# IMPORTANT - subprocesses inherit file descriptors when close_fds=False

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
				n //= a[0]
				out += [n]
			elif op=='split':
				out += [n]
				n *= a[0]
			else:
				out += [n]
		return out

	def init(self):
		cnt = self.proc_cnt()
		print(cnt)
		ops = self.ops
		pipe_id = {}
		pipe = {} # key -> stage,proc,kind
		process = {} # key -> pipe_id eg s3p0
		for s in reversed(range(len(ops))):
			cnt_here = cnt[s]
			cnt_next = 1 if s==len(ops)-1 else cnt[s+1]
			cnt_prev = 1 if s==0 else cnt[s-1]
			op = ops[s]
			print("stage:{0} op:{1[0]} pcnt:{2}".format(s,op,cnt_here))
			for p in range(cnt_here):
				if cnt_next < cnt_here:
					q = int(p//(cnt_here/cnt_next))
					s_next = s+2 # BUG - TODO proper offset
				elif cnt_next > cnt_here:
					n = int(cnt_next/cnt_here)
					q = list(range(p*n,(p+1)*n))
					s_next = s+1
				else:
					q = p
					s_next = s+1
				fi_id=['s{0}p{1}'.format(s,p) for p in p] if isinstance(p,list) else 's{0}p{1}'.format(s,p)
				fo_id=['s{0}p{1}'.format(s_next,q) for q in q] if isinstance(q,list) else 's{0}p{1}'.format(s_next,q)
				fe_id=''
				pipe_id[s,p,'fi'] = fi_id
				pipe_id[s,p,'fo'] = fo_id
				pipe_id[s,p,'fe'] = fe_id
				# ----------------------------------------------------------------------
				if 1 and op[0]!='join':
					print("  proc:{0} i:{1} o:{2}".format(p,fi_id,fo_id,fe_id))
					if op[0]=='pipe':
						fe = pipe.get(fe_id,sys.stderr)
						fi = sproc.PIPE if s>0 else sys.stdin
						fo = pipe.get(fo_id,sys.stdout)
						args = shlex.split(op[1][0])
						proc = sproc.Popen(args,stdin=fi,stdout=fo,stderr=fe,close_fds=False)
						pipe[fi_id] = proc.stdin
						process[fi_id] = proc
					if 0 and op[0]=='split': # multiprocessing SPLIT
						fe = pipe.get(fe_id,sys.stderr)
						fd_read,fd_write = os.pipe()
						fi_read = os.fdopen(fd_read,'rb')
						fi_write = os.fdopen(fd_write,'wb')
						fo_list = [pipe[fo_id] for fo_id in fo_id]
						out_fd_list = [f.fileno() for f in fo_list]
						proc = mproc.Process(target=split,args=(fd_read,out_fd_list))
						proc.wait = proc.join # single interface for waiting till process ends
						pipe[fi_id] = fi_write
						process[fi_id] = proc
						proc.start()
					if 1 and op[0]=='split': # subprocess SPLIT with file descriptor inheritance
						fe = pipe.get(fe_id,sys.stderr)
						fi = sproc.PIPE if s>0 else sys.stdin
						fo_list = [pipe[fo_id] for fo_id in fo_id]
						out_fd_list = [str(f.fileno()) for f in fo_list]
						args = ['python','split.py']+out_fd_list
						proc = sproc.Popen(args,stdin=fi,stdout=None,stderr=fe,close_fds=False)
						pipe[fi_id] = proc.stdin
						process[fi_id] = proc
					if 0 and op[0]=='split': # subprocess SPLIT with named pipes
						pass
		for k,proc in sorted(process.items()):
			print('waiting for',k)
			proc.wait()


def split(in_fd, out_fd_list): # for multiprocessing
	block_size = 1024
	fi = os.fdopen(in_fd,'rb')
	fo_list = [os.fdopen(fd,'wb') for fd in out_fd_list]
	while True:
		for fo in fo_list:
			block = fi.read(block_size)+fi.readline()
			fo.write(block)
			if len(block)<block_size: break
		else: continue
		break

#~ def pipe(fi,fo,fe,cfg):
	#~ cmd = cfg['cmd']
	#~ cmd_args = shlex.parse(cmd)
	#~ proc = subprocess.Popen(cmd_args)

job=(Job()
	#.pipe('cat test.txt')
	#.pipe('cat test.txt')
	#.pipe('''python -c "print('hello\\nworld\\n')"''')
	#.split(2)
	#.pipe('cat test.txt')
	#~ .split(2)
	#~ .pipe('cat')
	#~ .pipe('cat')
	#.join(2)
	#~ .pipe('cat')
	#~ .join(2)
	#.pipe('''python -c "import sys; open('usunmnie.txt','w').write(sys.stdin.read())"''')
	#.pipe('cat test.txt')
	#.pipe('empty')
	.split(2)
	.pipe('cat test.txt')
	.split(2)
	.pipe('empty')
	.join(4)
	.pipe('empty')
).init()
