import subprocess
from textwrap import dedent
from hashlib import sha1

# version x4 - header, app_name, echo

def pipe(*cmds, **kw):
	doc = kw.get('doc',[])
	cmd = ' | '.join(cmds)
	if doc:
		cmd += '\n'
		for d in doc:
			cmd += d.strip()+'\n'
		# TODO rstrip?
	return cmd


class host:
	def __init__(self, prefix='', run=True, echo=True):
		self._run = run
		self._echo = echo
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
		if self._echo:
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
		self.os("spark2-submit {1} {0}", script_path, spark_args)
		if remove:
			self.os('rm -f '+script_path)
	

	def extract_csv(self, path, sql, output_dir='', script_path='', app_name='utilx4', header=False, spark_args='', options='', remove='all'):
		tmp_name = sha1(sql).hexdigest()[:16]
		output_dir = output_dir or tmp_name
		script_path = script_path or '/tmp/{0}.py'.format(tmp_name)
		csv_options = '' if not options else ','+options
		code = """
			from pyspark.sql import SparkSession
			spark = SparkSession.builder.appName('{3}').getOrCreate()
			df = spark.sql("{0}")
			df.write.csv('{1}'{2},mode='overwrite',header={4})
			""".format(sql, output_dir, csv_options, app_name, header)
		
		self.spark_run(code, script_path, spark_args=spark_args, remove=remove in ['all','script'])
		
		# TODO pipe into ???
		self.dfs('text {0}/part* >{1} 2>{1}.log',output_dir,path) # getmerge?
		if remove.lower() in ['output','all']:
			self.dfs('rm -r -f {0}',output_dir)

if __name__=="__main__":
	h=host('ssh userxxx@aaa.bbb.ccc.ddd.pl',run=False)
	h.extract_csv('test.csv','select * from testdb.example_table limit 100',options="sep='|'")
