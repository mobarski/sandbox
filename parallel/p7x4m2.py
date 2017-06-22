## p7.py - parallel processing microframework
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: ex4 (simple fan-in of subprocess outputs)
##         mod2 (cmd line options)

from __future__ import print_function

# CMD LINE OPTIONS #########################################################################

import argparse

parser = argparse.ArgumentParser(description="P7 streaming utility - run command in parallel")
parser.add_argument('mapper',type=str,help='mapper command')
parser.add_argument('-i',type=int,default=1024,help='head buffer size for input data pump (1024)')
parser.add_argument('-o',type=int,default=1024,help='head buffer size for output data pump (1024)')
parser.add_argument('-b',type=int,default=4096,help='buffer size for subprocess (4096)')
parser.add_argument('-e',type=str,default='mapper{}.log',help='path template for stderr (logs), must contain {} which will be replaced by partition id (mapper{}.log)')
parser.add_argument('-n',type=int,default=4,help='number of mapper jobs (4)')

cmd_line_args = parser.parse_args()

# CONFIG ###################################################################################

CMD = cmd_line_args.mapper
N = cmd_line_args.n
ERR_PATH_TEMPLATE = cmd_line_args.e

BUFSIZE = cmd_line_args.b
HEAD_LEN_IN = cmd_line_args.i
HEAD_LEN_OUT = cmd_line_args.o

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
PIPE = subprocess.PIPE
for i in range(N):
	ctx[i] = {}
	log_path = ERR_PATH_TEMPLATE.format(i)
	log_file = open(log_path,'w')
	proc = subprocess.Popen(args, stdin=PIPE, stdout=PIPE, stderr=log_file, bufsize=BUFSIZE)
	ctx[i]['proc'] = proc
	# metadata
	ctx[i]['pid'] = proc.pid
	ctx[i]['t_start'] = time()
	ctx[i]['head_cnt_in'] = 0
	ctx[i]['head_cnt_out'] = 0
	ctx[i]['log_file'] = log_file
	ctx[i]['log_path'] = log_path
	# stats
	print("BEGIN  worker:{}  pid:{}".format(i,proc.pid), file=sys.stderr)

def pump_input():
	while True:
		for i in range(N):
			p = ctx[i]['proc']
			head = IN.read(HEAD_LEN_IN)
			p.stdin.write(head)
			ctx[i]['head_cnt_in'] += 1
			if len(head)<HEAD_LEN_IN: # End Of File
				break
			tail = IN.readline()
			p.stdin.write(tail)
		else: continue # not EOF
		
		# EOF -> close all input streams
		for i in range(N):
			ctx[i]['proc'].stdin.close()
		break


def pump_output():
	done = set()
	while True:
		for i in range(N):
			if i in done: continue
			p = ctx[i]['proc']
			head = p.stdout.read(HEAD_LEN_OUT)
			OUT.write(head)
			ctx[i]['head_cnt_out'] += 1
			if len(head)<HEAD_LEN_OUT: # End Of File
				done.add(i)
				p.wait() # End Of Process
				ctx[i]['t_stop'] = time()
				ctx[i]['run_time'] = ctx[i]['t_stop'] - ctx[i]['t_start']
				continue
			tail = p.stdout.readline()
			OUT.write(tail)
		if len(done)==N:
			return


# RUN DATA PUMPS
input_pump = threading.Thread(target=pump_input)
output_pump = threading.Thread(target=pump_output)
input_pump.start()
output_pump.start()
input_pump.join()
output_pump.join()

for i in range(N):
	ctx[i]['log_file'].close()

# stats
for i in range(N):
	print("END    worker:{}  pid:{}  run_time:{:.1f}s  in:{}  out:{}".format(i,proc.pid,ctx[i]['run_time'],ctx[i]['head_cnt_in'],ctx[i]['head_cnt_out']), file=sys.stderr)

print("\nRUN_TIME_TOTAL:{:.1f}s".format(time()-t0), file=sys.stderr)
