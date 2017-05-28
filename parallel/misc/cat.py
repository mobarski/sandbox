import sys
import os

fe=sys.stderr
fe.write('STDERR FD {0}\n'.format(fe.fileno()))

if sys.argv[1:]:
	for path in sys.argv[1:]:
		f=open(path,'r')
		sys.stdout.write(f.read())
		f.close()
else:
	sys.stdout.write(sys.stdin.read())
