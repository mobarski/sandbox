# cli - p7red reducer output inputs...

import io
import sys
from tempfile import TemporaryFile
import subprocess

cmd = 'python p7red.test.py' # sys.argv[0]
outpath = 'p7red.out.txt' # sys.argv[1]
inputs = ['p7red.test0.txt','p7red.test1.txt'] #sys.argv[2:]
combiner = 'sort | sort'


all_data = ''
for path in inputs:
	fi = open(path,'rb')
	if combiner:
		data = subprocess.check_output(combiner, stdin=fi, shell=True)
	else:
		data = fi.read()
	fi.close()
	all_data += data.decode()


lines = [line.strip() for line in all_data.split('\n') if line.strip()]
lines.sort()

fi = TemporaryFile()
fi.write('\n'.join(lines).encode())
fi.seek(0)
fo = open(outpath,'wb')
p = subprocess.Popen(cmd, stdin=fi, stdout=fo, shell=True)
#
p.wait()
