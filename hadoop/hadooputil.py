import subprocess
from textwrap import dedent


def run(cmd):
	print(cmd.strip())
	#return subprocess.check_call(cmd,shell=True)


def run_script(cmd_list):
	for cmd in cmd_list:
		run(cmd)


def pipe(*cmds, **kw):
	cmd = ' | '.join(cmds)
	if 'doc' in kw:
		cmd += '\n'
		for doc in kw['doc']:
			cmd += doc.rstrip()+'\n'
		# TODO rstrip?
	return cmd


class hadoop:
	def __init__(self, prefix=''):
		self.prefix = prefix.rstrip()+' ' if prefix else ''

	def os(self, cmd, *a, **kw):
		return self.prefix + cmd.format(*a,**kw)
		
	def cat(self, path):
		cmd = 'hdfs dfs -cat '+path
		return self.prefix + cmd

	def text(self, path):
		cmd = "hdfs dfs -text "+path
		return self.prefix + cmd

	def getmerge(self, source_path, target_path):
		cmd = "hdfs dfs -getmerge {0} {1}".format(source_path,target_path)
		return self.prefix + cmd

	def rm(self, path):
		cmd = 'hdfs dfs -rm -f '+path
		return self.prefix + cmd

	def rmr(self, path):
		cmd = 'hdfs dfs -rmr -f '+path
		return self.prefix + cmd

	def put_pipe(self, target_path):
		cmd = 'hdfs dfs -put - '+target_path
		return self.prefix + cmd

	def put(self, source_path, target_path):
		source = source_path
		target = target_path
		cmd = 'hdfs dfs -put {0} {1}'.format(source,target)
		return self.prefix + cmd
	
	def spark(self, args):
		cmd = 'spark2-submit '+args
		return self.prefix + cmd
	
	def host_write(self, path, text):
		local = hadoop()
		return pipe(local.os('cat <<EOF'),self.os('cat >'+path),doc=[text,'EOF'])
	

	# scripts

	def spark_load(self): pass # TODO
	
	def spark_run(self, code, script_path, spark_args='', remove='all'):
		# TODO random/dynamic script path
		script = dedent(code).strip()
		yield self.host_write(script_path,script)
		yield self.spark("{0} {1}".format(script_path, spark_args))
		if remove.lower() in ['script','all']:
			yield self.os('rm -f '+script_path)
	
	def extract_csv(self, table, output_dir, script_path, spark_args='', remove='none'):
		# TODO random/dynamic output_dir
		# TODO clean output dir at start
		# TODO csv args
		code = """
			spark.table('{0}').write.csv('{1}')
			""".format(table, output_dir)
		
		for cmd in self.spark_run(code, script_path, spark_args=spark_args, remove=remove):
			yield cmd
		
		# TODO pipe into ???
		yield self.text(output_dir+'/part*') # getmerge?
		if remove.lower() in ['output','all']:
			yield self.rmr(output_dir)
		

h=hadoop('ssh userxxx@aaa.bbb.ccc.ddd.pl')

#pipe(p.cat('../costam.txt'), h.put_pipe('/home/mobarki/xxx'))
#pipe(h.put('xxx','ttt'))
#pipe(h.spark2('xxx.py {0}','v13'))
#pipe(h.put('<<EOF','/tmp/costam.txt'),h.put('<<EOF','/tmp/xxx'),doc=['to\njest\ntest','EOF','zzz\nxxx','EOF'])

script = h.extract_csv('testdb.example_table','/sample/output/dir','test_script_path',remove='all')
run_script(script)
