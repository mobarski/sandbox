import subprocess
import tempfile

# RETL/REMETL (Remote ETL)

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
			out = self.run_text(self.get_after())
			self.after = []
	
	def set(self, var_name, value):
		"set variable value"
		self.var[var_name] = value.format(**self.var)
		return self
	
	def tmp(self, var_name, text='', eof='EOF'):
		"create temporary file and store its path in a variable"
		path = '/tmp/'+random_name(self.host, text, var_name) # TODO
		self.var[var_name] = path
		if text:
			self.script += ['cat >{0} <<{2}\n{1}\n{2}'.format(path,text.format(**self.var),eof)]
		else:
			self.script += ['touch {0}'.format(path)]
		return self
	
	def cmd(self, text):
		"execute command"
		self.script += [text.format(**self.var)]
		return self

	def download(self, local_path, remote_path): # czy odwrotnie argumenty?
		cmd = '{0} {1}:{2} {3}'.format(self.scp, self.host, remote_path.format(**self.var), local_path.format(**self.var))
		out = subprocess.check_output(cmd, shell=True) # TODO czy check_call stdout na stdout?
		return out
	
	def upload(self, local_path, remote_path): # czy odwrotnie argumenty?
		cmd = '{0} {3} {1}:{2}'.format(self.scp, self.host, remote_path.format(**self.var), local_path.format(**self.var))
		out = subprocess.check_output(cmd, shell=True) # TODO czy check_call stdout na stdout?
		return out

	def run(self):
		out = self.run_text(self.get_script())
		self.script = []
		return out

	def get_script(self):
		return '\n'.join(self.script) + '\n'

	def get_after(self):
		return '\n'.join(self.after) + '\n'

	def run_text(self, text):
		cmd = self.ssh+' '+self.host
		with tempfile.TemporaryFile() as f:
			f.write(text)
			f.seek(0)
			out = subprocess.check_output(cmd, stdin=f, shell=True) # TODO czy check_call stdout na stdout?
		return out

class hadoop_host(host): pass


# --- helpers

def random_name(text='',text2='',label='noname',length=6):
	import random
	import hashlib
	out = hashlib.sha1(text).hexdigest()[:length]+'-'
	out += hashlib.sha1(text2).hexdigest()[:length]+'-'
	for i in range(length):
		out += random.choice('3')
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

