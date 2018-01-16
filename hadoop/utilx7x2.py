import subprocess
import tempfile

# --- helpers
def random_name(text='',text2='',length=6):
	import random
	import hashlib
	out = hashlib.sha1(text).hexdigest()[:length]+'-'
	out += hashlib.sha1(text2).hexdigest()[:length]+'-'
	for i in range(length):
		out += random.choice('qwertyuiopasdfghjklzxcvbnm1234567890')
	return out

class host:	
	def __init__(self,ssh_cmd=''):
		self.ssh_cmd = ssh_cmd
		self.variable = {}
		self.before = []
		self.main = []
		self.after  = []
	
	def set(self,name,value):
		"set variable that will be available in other steps"
		self.variable[name] = value.format(**self.variable)
		return self
	
	def tmp(self,name,text='',eof='EOF',remove=True):
		"create temporary file with given text"
		path = '/tmp/'+random_name(self.ssh_cmd,text)
		self.variable[name] = path
		if text:
			self.before += ['cat >{0} <<{2}\n{1}\n{2}'.format(path,text.format(**self.variable),eof)]
		else:
			self.before += ['touch {0}'.format(path)]
		if remove:
			self.after += ['rm {0}'.format(path)]
		return self
	
	def cmd(self,text):
		"execute command"
		self.main += [text.format(**self.variable)]
		return self
	
	def get_full_script(self):
		before = '\n'.join(self.before)
		main = '\n'.join(self.main)
		after = '\n'.join(self.after)
		return '\n'.join([before,main,after]) + '\n'
	
	def run(self):
		script = self.get_full_script()
		with tempfile.TemporaryFile() as f:
			f.write(script)
			f.seek(0)
			out = subprocess.check_output(self.ssh_cmd,stdin=f,shell=True) # TODO czy check_call stdout na stdout?
		return out

h=host('cat >output.txt')
h.set('hive','beeline -u "jdbc:hive2://xxx.aaa.bbb.ccc:10000/;principal=hive/xxx.aaa.bbb@zzz.vvv.bbb?mapreduce.job.queuename=abcd" --showHeader=false')
h.tmp('f1','xxx')
h.tmp('f2','yyy')
h.tmp('f3','zzz')
h.tmp('f4',remove=False)
h.cmd('{hive} -f {f1} >{f4}')
s = h.get_full_script()
print(s)
h.run()
