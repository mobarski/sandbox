import subprocess
import tempfile

# RETL (Remote ETL)

class host:	
	def __init__(self, host='', ssh='ssh', scp='scp'):
		self.host = host
		self.ssh = ssh
		self.scp = scp
		self.variable = {'host':host}
		self.before = [] # czy to jest potrzebne?
		self.main = []
		self.after  = []
	
	def set(self, var_name, value):
		"set variable value"
		self.variable[var_name] = value.format(**self.variable)
		return self
	
	def tmp(self, var_name, text='', eof='EOF', remove=True):
		"create temporary file and store its path in a variable"
		path = '/tmp/'+random_name(self.host, text, var_name) # TODO
		self.variable[var_name] = path
		if text:
			self.before += ['cat >{0} <<{2}\n{1}\n{2}'.format(path,text.format(**self.variable),eof)]
		else:
			self.before += ['touch {0}'.format(path)]
		if remove:
			self.after += ['rm {0}'.format(path)]
		return self
	
	def cmd(self, text):
		"execute command"
		self.main += [text.format(**self.variable)]
		return self
	
	def run(self):
		cmd = self.ssh+' '+self.host
		script = self.get_full_script()
		with tempfile.TemporaryFile() as f:
			f.write(script)
			f.seek(0)
			out = subprocess.check_output(cmd, stdin=f, shell=True) # TODO czy check_call stdout na stdout?
		return out

	def download(self, local_path, remote_path): # czy odwrotnie argumenty?
		v = self.variable
		cmd = '{0} {1}:{2} {3}'.format(self.scp, self.host, remote_path.format(**v), local_path.format(**v))
		out = subprocess.check_output(cmd, shell=True) # TODO czy check_call stdout na stdout?
		return out
	
	def upload(self, local_path, remote_path): # czy odwrotnie argumenty?
		v = self.variable
		cmd = '{0} {3} {1}:{2}'.format(self.scp, self.host, remote_path.format(**v), local_path.format(**v))
		out = subprocess.check_output(cmd, shell=True) # TODO czy check_call stdout na stdout?
		return out

	def get_full_script(self):
		before = '\n'.join(self.before)
		main = '\n'.join(self.main)
		after = '\n'.join(self.after)
		return '\n'.join([before,main,after]) + '\n'

# --- helpers
def random_name(text='',text2='',label='noname',length=6):
	import random
	import hashlib
	out = hashlib.sha1(text).hexdigest()[:length]+'-'
	out += hashlib.sha1(text2).hexdigest()[:length]+'-'
	for i in range(length):
		out += random.choice('qwertyuiopasdfghjklzxcvbnm1234567890')
	out += '-'+label
	return out

if __name__=="__main__":
	h=host('','cat')
	h.set('hive','beeline -u "jdbc:hive2://xxx.aaa.bbb.ccc:10000/;principal=hive/xxx.aaa.bbb@zzz.vvv.bbb?mapreduce.job.queuename=abcd" --showHeader=false')
	h.set('x','abc')
	h.set('y','test {x} ok')
	h.tmp('f1','xxx')
	h.tmp('f2','yyy')
	h.tmp('f3','{y}')
	h.tmp('f4',remove=False)
	h.cmd('{hive} -f {f1} >{f4}')
	s = h.get_full_script()
	print(s)
	h.run()
