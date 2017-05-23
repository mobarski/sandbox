import p7
from pprint import pprint
cmd = '''python -c "import sys,os; fi=os.fdopen(0,'rb'); fo=os.fdopen(1,'wb'); fo.write(fi.read())" '''
f_in = "test.txt"
f_out = 'test/out.part.txt'
f_log = 'test/log.part.txt'
job=p7.Job(cmd,f_in,4,f_out,f_log,block_size=10)
#pprint(job.meta)
job.run()
