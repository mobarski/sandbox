import subprocess
import tempfile
import textwrap

# NAME: RETL/REETL/REMETL (remote ETL)
# NAME: HOSH (Hadoop over SSH)
# NAME: REHAT (remote Hadoop utils/tools)

class host:	
	def __init__(self, host='', ssh='ssh', scp='scp'):
		self.host = host
		self.ssh = ssh
		self.scp = scp
		self.var = {'host':host}
		self.script = []
		self.after  = []
	
	def __enter__(self):
		return self
	
	def __exit__(self,et,ev,tb):
		self.clean()
	
	def clean(self):
		"remove temporary files"
		if self.after:
			after = self.get_after()
			print(after)
			out = self.execute_script(after)
			self.after = []
	
	def set(self, var_name, value):
		"set variable value"
		self.var[var_name] = value.format(**self.var)
		return self
	
	def get(self, var_name):
		"get variable value or None if var doesnt exists"
		return self.var.get(var_name)
	
	def tmp(self, var_name='', text='', eof='EOF', prefix='/tmp/', suffix='', dedent=True):
		"create temporary file and store its path in a variable"
		if dedent:
			text = textwrap.dedent(text).strip()
		path = prefix + random_name(self.host, text, var_name) + suffix
		if var_name:
			self.var[var_name] = path
		if text:
			self.script += ['cat >{0} <<{2}\n{1}\n{2}'.format(path,text.format(**self.var),eof)]
		else:
			self.script += ['touch {0}'.format(path)]
		return path
	
	def cmd(self, text):
		"add command to the main script"
		self.script += [text.format(**self.var)]
		return self

	def download(self, local_path, remote_path): # czy odwrotnie argumenty?
		"download file from host"
		self.run()
		cmd = '{0} {1}:{2} {3}'.format(self.scp, self.host, remote_path.format(**self.var), local_path.format(**self.var))
		print(cmd)
		out = subprocess.check_call(cmd, shell=True) # TODO check_call czy check_output
		return out
	
	def upload(self, local_path, remote_path): # czy odwrotnie argumenty?
		"upload file to host"
		cmd = '{0} {3} {1}:{2}'.format(self.scp, self.host, remote_path.format(**self.var), local_path.format(**self.var))
		print(cmd)
		out = subprocess.check_call(cmd, shell=True) # TODO check_call czy check_output
		return out

	def run(self):
		"run main script"
		if self.script:
			script = self.get_script()
			print(script)
			out = self.execute_script(script)
		else:
			out = None
		self.script = []
		return out

	def get_script(self):
		return '\n'.join(self.script) + '\nexit\n'

	def get_after(self):
		return '\n'.join(self.after) + '\nexit\n'

	def execute_script(self, text):
		"immediate execution of commands passed via stdin to ssh"
		cmd = self.ssh+' '+self.host
		with tempfile.TemporaryFile() as f:
			f.write(text)
			f.seek(0)
			out = subprocess.check_call(cmd, stdin=f, shell=True) # TODO check_call czy check_output
		return out

	def execute(self, cmd, stdin=None, before=''):
		"immediate execution of command passed via args to ssh"
		full_cmd = before + self.ssh +' '+ self.host +' '+ cmd
		out = subprocess.check_call(full_cmd, stdin=stdin, shell=True)
		return out

# ------------------------------------------------------------------------------

import hashlib
import re

class hadoop_host(host):
	def extract_csv(self, path, table, output_dir='', config={}, spark_args='', aux='',
			sep=',', header=False, quote=None, escape=None, escape_quotes=None, quote_all=None, null_value=None, mode=None,
			select=None, drop=None, where=None, limit=None,
			remove='all'):
		# TODO column names
		
		tmp_name = hashlib.sha1(table.encode()+self.host).hexdigest()[:16]
		output_dir = output_dir or tmp_name
		app_config_str = ''.join([".config('{0}','{1}')".format(k,v) for k,v in config.items()])
		
		# csv options
		csv_aux = ""
		if quote		is not None: csv_aux += ''',quote="""{0}"""'''.format(quote)
		if escape		is not None: csv_aux += ''',escape="""{0}"""'''.format(escape)
		if null_value 		is not None: csv_aux += ''',nullValue="""{0}"""'''.format(null_value)
		if escape_quotes	is not None: csv_aux += ''',escapeQuotes={0}'''.format(escape_quotes)
		if quote_all 		is not None: csv_aux += ''',quoteAll={0}'''.format(quote_all)
		
		# df options 
		df_aux = aux
		if select:
			df_aux += '''.selectExpr({0})'''.format(','.join(["'''{0}'''".format(x) for x in select]))
		if where:
			df_aux += """.where('''{0}''')""".format(where)
		if drop:
			df_aux += """.drop({0})""".format(','.join(["'''{0}'''".format(x) for x in drop]))
		if limit:
			df_aux += '.limit({0})'.format(limit)
		
		code = """
			from pyspark.sql import SparkSession
			spark = SparkSession.builder.appName('RemoteETL {1}'){6}.getOrCreate()
			df = spark.table('''{0}'''){2}
			df.write.csv('{1}',mode='overwrite',header={4},sep='''{5}'''{3})
			""".format(table, output_dir, df_aux, csv_aux, header, sep, app_config_str)
		code = re.sub('(?m)^\s+','',code) #UGLY FIX for multiline indented sql code
		
		self.cmd('hdfs dfs -rm -r -f {0}'.format(output_dir))
		script_path = self.tmp(text=code, suffix='.py')
		self.cmd("spark2-submit {} {}".format(spark_args, script_path))
		self.run()
		
		self.download_from_hdfs(path, output_dir)
		if remove.lower() in ['output','all']:
			self.after += ['hdfs dfs -rm -r -f {0}'.format(output_dir)]

	def download_from_hdfs(self, local_path, hdfs_path):
		self.execute('"hdfs dfs -text {0}/part*" >{1}'.format(hdfs_path, local_path))
		
	def upload_into_hdfs(self, local_path, hdfs_path):
		self.execute('hdfs dfs -put - {0}'.format(hdfs_path), stdin=open(local_path,'r'))

	def pipe_from_hdfs(self, pipe_cmd, hdfs_path):
		self.execute('"hdfs dfs -text {0}/part*" | {1}'.format(hdfs_path, pipe_cmd))
		
	def pipe_into_hdfs(self, pipe_cmd, hdfs_path):
		self.execute('hdfs dfs -put - {0}'.format(hdfs_path), before=pipe_cmd+' | ')

# --- helpers

def random_name(text='',text2='',label='',length=6):
	import random
	out = hashlib.sha1(text).hexdigest()[:length]
	out += '-'+hashlib.sha1(text2).hexdigest()[:length]
	for i in range(length):
		out += random.choice('3')
	if label:
		out += '-'+label
	return out

# ------------------------------------------------------------------------------

if __name__=="__main__":
	with host('','cat','echo') as h:
		h.set('hive','beeline -u "jdbc:hive2://xxx.aaa.bbb.ccc:10000/;principal=hive/xxx.aaa.bbb@zzz.vvv.bbb?mapreduce.job.queuename=abcd" --showHeader=false')
		h.set('x','abc')
		h.set('y','test {x} ok')
		h.tmp('f1','xxx')
		h.tmp('f2','yyy')
		h.tmp('f3','{y}')
		h.tmp('f4')
		h.cmd('{hive} -f {f1} >{f4}')
		s = h.get_script()
		print(s)
		h.run()
		h.download('test_f3.txt','{f3}')

