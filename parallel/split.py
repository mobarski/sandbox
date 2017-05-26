import sys
import os
import io

BLOCK_SIZE = 1024

fi = sys.stdin
fe = sys.stderr
fd_list = list(map(int,sys.argv[1:]))
fe.write('ARGV\t{0}\n'.format(sys.argv))
fe.write('FD_LIST\t{0}\n'.format(fd_list))
fo_list = [os.fdopen(fd,'wb') for fd in fd_list]

while fo_list:
	for fo in fo_list:
		block = fi.read(BLOCK_SIZE)+fi.readline()
		fo.write(block)
		fe.write(block)
		if len(block)<BLOCK_SIZE:
			#~ for fd in fd_list:
				#~ os.close(fd)
			for f in fo_list:
				f.close()
			break
	else: continue
	break
os.close(0)
os.close(1)
os.close(2)
