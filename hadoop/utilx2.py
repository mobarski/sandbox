import subprocess
from textwrap import dedent

def pipe(*cmds, doc=[]):
	cmd = ' | '.join(cmds)
	if doc:
		cmd += '\n'
		for d in doc:
			cmd += d.strip()+'\n'
		# TODO rstrip?
	return cmd


class host:
	def __init__(self, prefix='', run=False):
		self._run = run
		self.prefix = prefix.rstrip()+' ' if prefix else ''

	def os(self, cmd, *a, **kw):
		full_cmd = self._os(cmd,*a,**kw)
		return self.run(full_cmd)

	def dfs(self, cmd, *a, **kw):
		full_cmd = self._dfs(cmd,*a,**kw)
		return self.run(full_cmd)
			
	def write(self, path, text, eof='EOF'):
		full_cmd = self._write(path, text, eof)
		return self.run(full_cmd)

	def run(self, cmd):
		print(cmd)
		if self._run:
			return subprocess.check_call(cmd,shell=True)

	# full command prepparation
	
	def _os(self, cmd, *a, **kw):
		return self.prefix + cmd.format(*a,**kw)

	def _dfs(self, cmd, *a, **kw):
		return self.prefix + 'hdfs dfs -'+cmd.lstrip().format(*a,**kw)

	def _write(self, path, text, eof='EOF'):
		return pipe(
			'cat <<'+eof,
			self._os('"cat >{0}"'.format(path)),
			doc=[text,eof]
			)

	# scripts

	def spark_load(self): pass # TODO
	
	def spark_run(self, code, script_path, spark_args='', remove=True):
		# TODO random/dynamic script path
		script = dedent(code).strip()
		self.write(script_path, script)
		self.os("spark2-submit {0} {1}", script_path, spark_args)
		if remove:
			self.os('rm -f '+script_path)
	
	def extract_csv(self, table, output_dir='', script_path='', spark_args='', options='', remove='all'):
		tmp_name = table.lower().replace('.','_')
		output_dir = output_dir or tmp_name
		script_path = script_path or '~/{0}.py'.format(tmp_name)
		csv_options = '' if not options else ','+options
		code = """
			from pyspark.sql import SparkSession
			spark = SparkSession.builder.appName('TODO').getOrCreate()
			spark.table('{0}').write.csv('{1}'{2})
			""".format(table, output_dir, csv_options)
		
		self.spark_run(code, script_path, spark_args=spark_args, remove=remove in ['all','script'])
		
		# TODO pipe into ???
		self.dfs('text {0}/part*',output_dir) # getmerge?
		if remove.lower() in ['output','all']:
			self.dfs('rm -r -f {0}',output_dir)

if __name__=="__main__":
	h=host('ssh userxxx@aaa.bbb.ccc.ddd.pl',run=False)
	h.dfs('put {0} {1}','xxx','yyy')
	h.write('/tmp/xxx','to\njest\ntest')

	#pipe(p.cat('../costam.txt'), h.put_pipe('/home/mobarki/xxx'))
	#pipe(h.put('xxx','ttt'))
	#pipe(h.spark2('xxx.py {0}','v13'))
	#pipe(h.put('<<EOF','/tmp/costam.txt'),h.put('<<EOF','/tmp/xxx'),doc=['to\njest\ntest','EOF','zzz\nxxx','EOF'])

	h.extract_csv('testdb.example_table',options="sep='|'")

