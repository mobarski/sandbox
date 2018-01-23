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
		#self.run() # ?????
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
	
	# TODO kolejnosc argumentow - najpiers text potem var
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
		full_cmd = full_cmd.format(**self.var)
		# TODO if type(stdin) is str: tempfile
		print(full_cmd)
		out = subprocess.check_call(full_cmd, stdin=stdin, shell=True)
		return out

# ------------------------------------------------------------------------------

import hashlib
import re

class hadoop_host(host):
	
	def __init__(self, addr='', ssh='ssh', scp='scp'):
		host.__init__(self, addr, ssh, scp)
		self.var['hive'] = 'hive'
		self.var['load_dir'] = '/tmp'

	def download_from_hdfs(self, local_path, hdfs_path):
		self.run()
		self.execute('"hdfs dfs -text {0}/[^.]*" >{1}'.format(hdfs_path, local_path))
		
	def upload_into_hdfs(self, local_path, hdfs_path):
		self.run()
		self.execute('hdfs dfs -put - {0}'.format(hdfs_path), stdin=open(local_path,'r'))

	def pipe_from_hdfs(self, pipe_cmd, hdfs_path):
		self.run()
		self.execute('"hdfs dfs -text {0}/[^.]*" | {1}'.format(hdfs_path, pipe_cmd))
		
	def pipe_into_hdfs(self, pipe_cmd, hdfs_path):
		self.run()
		self.execute('hdfs dfs -put - {0}'.format(hdfs_path), before=pipe_cmd+' | ')

	def import_csv(self, path, table, columns, sep=','):
		# TODO zalozenie tabeli w konkretnym miejsu i upload partycji???
		# TODO elegancka obsluga columns!!!
		# TODO table comment???
		name = random_name(self.host, path+' '+table, 'import')
		hdfs_path = '{}/{}'.format(self.var['load_dir'],name)
		
		self.cmd('hdfs dfs -rm -r -f '+hdfs_path).run() # TODO jako opcja
		self.upload_into_hdfs(path, hdfs_path)
		script = """
			DROP TABLE if exists {table};
			CREATE TABLE {table}
				({columns})
				ROW FORMAT delimited fields terminated by '{sep}'
				;
			LOAD DATA
				INPATH '{hdfs_path}'
				OVERWRITE INTO TABLE {table}
				;
			
		""".format(**locals())
		path = self.tmp(text=script, suffix='.sql')
		self.cmd('{hive} -f '+path)
		self.after += ['hdfs dfs -rm -r -f '+hdfs_path] # TODO jako opcja?
		self.run()
	
	def extract_csv(self, path, sql, sep=','):
		name = random_name(self.host,sql,'extract')
		hdfs_path = '{}/{}'.format(self.var['load_dir'],name)
		
		self.cmd('hdfs dfs -rm -r -f '+hdfs_path) # TODO jako opcja?
		script = """
		insert overwrite directory '{hdfs_path}'
			row format delimited fields terminated by '{sep}'
			stored as textfile
			
			{sql}
			;
		""".format(**locals())
		sql_path = self.tmp(text=script, suffix='.sql')
		self.cmd('{hive} -f '+sql_path)
		self.after += ['hdfs dfs -rm -r -f '+hdfs_path] # TODO jako opcja?
		self.download_from_hdfs(path,hdfs_path)

# --- helpers

def random_name(text='',text2='',label='',length=6):
	import random
	out = hashlib.sha1(text).hexdigest()[:length]
	out += '-'+hashlib.sha1(text2).hexdigest()[:length]
	for i in range(length):
		out += random.choice('qwertyuiopasdfghjklzxcvbnm1234567890')
	if label:
		out += '-'+label
	return out

def columns(col_str,types={},sep1=' ',sep2=':',default='string'):
	# TODO comments
	out = []
	for name_type in col_str.split(sep1):
		name,t = (name_type+sep2).split(sep2)[:2]
		t = types.get(t,default)
		out += [(name,t)]
	return ',  '.join([' '.join(c) for c in out])

# ------------------------------------------------------------------------------

def test1():
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


def test2():
	print(columns('a b c d:i e:i f:ai',types={'i':'int','ai':'array<int>'}))

def test3():
	with hadoop_host('','cat','cat') as h:
		h.set('hive','beeline')
		cols = columns('a b c d')
		h.import_csv('ppp','ttt','idir',cols)
		print(h.get_script())

if __name__=="__main__":
	test3()
