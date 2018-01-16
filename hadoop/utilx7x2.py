class host:	
	def __init__(self,ssh_cmd=''):
		self.ssh_cmd = ssh_cmd
		self.variable = {}
		self.before = [] # TODO zawiera polecenia czy funkcje pythona?
		self.script = []
		self.after  = []
	
	def set(self,name,value):
		"set variable that will be available in other steps"
		self.variable[name] = value
		return self
	
	def tmp(self,name,text):
		"create temporary file with given text"
		path = '/tmp/'+self.random_name()
		self.variable[name] = path
		self.before += ['cat >{0}'.format(path)] # TODO write(text.format(**self.variable))
		self.after += ['rm {0}'.format(path)]
		return self
	
	def cmd(self,text):
		"execute command"
		self.script += [text]
		return self
	
	# --- helpers
	def random_name(self,length=8):
		import random
		import hashlib
		out = hashlib.sha1(self.ssh_cmd).hexdigest()[:length]+'-'
		for i in range(length):
			out += random.choice('qwertyuiopasdfghjklzxcvbnm1234567890')
		return out

	# ---
	
	def get(self):
		before = '\n'.join(self.before).format(**self.variable)
		script = '\n'.join(self.script).format(**self.variable)
		after = '\n'.join(self.after).format(**self.variable)
		return [before,script,after]
	
	def run(self):
		pass # TODO before
		pass # TODO script
		pass # TODO after

h=host()
h.tmp('f1','xxx')
h.set('hive','beeline -u "jdbc:hive2://xxx.aaa.bbb.ccc:10000/;principal=hive/xxx.aaa.bbb@zzz.vvv.bbb?mapreduce.job.queuename=abcd" --showHeader=false')
h.cmd('{hive} -f {f1}')
s = h.get()
print(s)
