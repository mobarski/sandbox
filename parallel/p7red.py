# cli - p7red reducer output inpaths...

import io
import sys
from tempfile import TemporaryFile
import subprocess

if 0:
	cmd = 'python p7red.test.key.py'
	outpath = 'p7red.out.txt'
	inpaths = ['p7red.test0.txt','p7red.test1.txt']
	logpath = ''
	combiner = 'sort | sort'
else:
	if sys.version < '2.7':
		import optparse
		# TODO
	else:
		import argparse
		parser = argparse.ArgumentParser(description="p7red - P7 reducer job executor")
		parser.add_argument('reducer',type=str,help='reducer command')
		parser.add_argument('-i',type=str,default='',help='paths for stdin')
		parser.add_argument('-o',type=str,default='',help='path for stdout')
		parser.add_argument('-e',type=str,default='',help='path for stderr (logs)')
		parser.add_argument('-c',type=str,default='',help='combiner command')
		# TODO: merge / sort controls (current=sort)
		cmd_line_args = parser.parse_args()
	cmd = cmd_line_args.reducer
	outpath = cmd_line_args.o
	inpaths = cmd_line_args.i
	logpath = cmd_line_args.e
	combiner = cmd_line_args.c


fe = open(logpath,'wb') if logpath else sys.stderr
all_data = ''
for path in inpaths:
	fi = open(path,'rb')
	if combiner:
		data = subprocess.check_output(combiner, stdin=fi, stderr=fe, shell=True)
	else:
		data = fi.read()
	fi.close()
	all_data += data.decode()


lines = [line.strip() for line in all_data.split('\n') if line.strip()]
lines.sort()

fi = TemporaryFile()
fi.write('\n'.join(lines).encode())
fi.seek(0)
fo = open(outpath,'wb') if outpath else sys.stdout
p = subprocess.Popen(cmd, stdin=fi, stdout=fo, stderr=fe, shell=True)
#
p.wait()
