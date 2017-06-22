## p7.py - parallel processing microframework
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: ex4 (simple fan-in of subprocess outputs)
##         mod2 (cmd line options)
##         mod3 (2.6 compatibility)
##         mod4 (no fan-in)

from __future__ import print_function

# CMD LINE OPTIONS #########################################################################
import sys

if sys.version < '2.7':
	import optparse
	parser = optparse.OptionParser(description="P7 streaming utility - run command in parallel")
	parser.add_option('-i',type=int,default=1024,help='head buffer size for input data pump (1024)')
	parser.add_option('-b',type=int,default=4096,help='buffer size for subprocess (4096)')
	parser.add_option('-o',type=str,default='mapper{0}.out',help='path template for stdout, must contain {0} which will be replaced by partition id (mapper{0}.out)')
	parser.add_option('-e',type=str,default='mapper{0}.log',help='path template for stderr (logs), must contain {0} which will be replaced by partition id (mapper{0}.log)')
	parser.add_option('-n',type=int,default=4,help='number of mapper jobs (4)')
	options,args = parser.parse_args()
	cmd_line_args = options
	cmd_line_args.mapper = ' '.join(args)
else:
	import argparse
	parser = argparse.ArgumentParser(description="P7 streaming utility - run command in parallel")
	parser.add_argument('mapper',type=str,help='mapper command')
	parser.add_argument('-i',type=int,default=1024,help='head buffer size for input data pump (1024)')
	parser.add_argument('-b',type=int,default=4096,help='buffer size for subprocess (4096)')
	parser.add_argument('-o',type=str,default='mapper{0}.out',help='path template for stdout, must contain {0} which will be replaced by partition id (mapper{0}.out)')
	parser.add_argument('-e',type=str,default='mapper{}.log',help='path template for stderr (logs), must contain {} which will be replaced by partition id (mapper{}.log)')
	parser.add_argument('-n',type=int,default=4,help='number of mapper jobs (4)')
	cmd_line_args = parser.parse_args()

if 0:
	print(cmd_line_args, file=sys.stderr)

# CONFIG ###################################################################################

CMD = cmd_line_args.mapper
N = cmd_line_args.n
ERR_PATH_TEMPLATE = cmd_line_args.e
OUT_PATH_TEMPLATE = cmd_line_args.o

BUFSIZE = cmd_line_args.b
HEAD_LEN = cmd_line_args.i

# END OF CONFIG ############################################################################

import subprocess
import threading
import shlex
import sys
from select import select
from time import time

t0 = time()

IN = sys.stdin
OUT = sys.stdout
LOG = sys.stderr

ctx = {}

print("\nP7 START\n", file=sys.stderr) # stats
args = shlex.split(CMD)
print("ARGS {0}\n".format(args), file=sys.stderr) # stats
PIPE = subprocess.PIPE
for i in range(N):
	ctx[i] = {}
	log_path = ERR_PATH_TEMPLATE.format(i)
	log_file = open(log_path,'w')
	out_path = OUT_PATH_TEMPLATE.format(i)
	out_file = open(out_path,'w')
	proc = subprocess.Popen(args, stdin=PIPE, stdout=out_file, stderr=log_file, bufsize=BUFSIZE)
	ctx[i]['proc'] = proc
	# metadata
	ctx[i]['pid'] = proc.pid
	ctx[i]['t_start'] = time()
	ctx[i]['head_cnt_in'] = 0
	ctx[i]['log_file'] = log_file
	ctx[i]['log_path'] = log_path
	# stats
	print("BEGIN  worker:{0}  pid:{1}".format(i,proc.pid), file=sys.stderr)

def pump_input():
	while True:
		for i in range(N):
			p = ctx[i]['proc']
			head = IN.read(HEAD_LEN)
			p.stdin.write(head)
			ctx[i]['head_cnt_in'] += 1
			if len(head)<HEAD_LEN: # End Of File
				break
			tail = IN.readline()
			p.stdin.write(tail)
		else: continue # not EOF
		
		# EOF -> close all input streams
		for i in range(N):
			ctx[i]['proc'].stdin.close()
		break


# RUN DATA PUMP
input_pump = threading.Thread(target=pump_input)
input_pump.start()
input_pump.join()

for i in range(N):
	ctx[i]['proc'].wait()
	ctx[i]['log_file'].close()

# stats
for i in range(N):
	print("END    worker:{0}  pid:{1}  in:{2}".format(i,ctx[i]['pid'],ctx[i]['head_cnt_in']), file=sys.stderr)

print("\nRUN_TIME_TOTAL:{0:.1f}s".format(time()-t0), file=sys.stderr)
