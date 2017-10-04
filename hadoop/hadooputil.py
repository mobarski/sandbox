import subprocess

def run(cmd):
	print(cmd)
	#return subprocess.check_call(cmd,shell=True)

def pipe(*cmds):
	cmd = ' | '.join(cmds)
	return run(cmd)


class posix:
	def __init__(self, prefix=''):
		self.prefix = prefix
	
	def cat(self, path, *a, **kw):
		cmd = 'cat '+path.format(*a,**kw)
		return self.prefix + cmd


class hadoop:
	def __init__(self, prefix=''):
		self.prefix = prefix.rstrip()+' ' if prefix else ''

	def cat(self, path, *a, **kw):
		cmd = 'hdfs dfs -cat '+path.format(*a,**kw)
		return self.prefix + cmd

	def rm(self, path, *a, **kw):
		cmd = 'hdfs dfs -rm -f '+path.format(*a,**kw)
		return self.prefix + cmd

	def put_pipe(self, target_path, *a, **kw):
		cmd = 'hdfs dfs -put - '+target_path.format(*a,**kw)
		return self.prefix + cmd

	def put(self, source_path, target_path, *a, **kw):
		source = source_path.format(*a,**kw)
		target = target_path.format(*a,**kw)
		cmd = 'hdfs dfs -put {0} {1}'.format(source,target)
		return self.prefix + cmd
	
	def spark(self, args, *a, **kw):
		cmd = 'spark-submit '+args.format(*a,**kw)
		return self.prefix + cmd
	
	def spark2(self, args, *a, **kw):
		cmd = 'spark2-submit '+args.format(*a,**kw)
		return self.prefix + cmd
	
	def spark_load(self, *a, **kw):
		pass

p=posix()
h=hadoop('ssh userxxx@aaa.bbb.ccc.ddd.pl')

pipe(p.cat('../costam.txt'), h.put_pipe('/home/mobarki/xxx'))
pipe(h.put('xxx','ttt'))
pipe(h.spark2('xxx.py {0}','v13'))
