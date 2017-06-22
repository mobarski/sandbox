## p7.py - parallel processing microframework
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: ex4 (simple fan-in of subprocess outputs)

from __future__ import print_function

# CONFIG ###################################################################################

HEAD_LEN_IN = 2
HEAD_LEN_OUT = 100
BUFSIZE = 4096

CMD = "python -c 'import sys; sys.stdout.write(sys.stdin.read())'"
N = 4

# END OF CONFIG ############################################################################

import subprocess
import threading
import shlex
import sys
from select import select
from time import time

IN = sys.stdin
OUT = sys.stdout
OUT = open('test/out.txt','wb')
LOG = sys.stderr

ctx = {}

args = shlex.split(CMD)
PIPE = subprocess.PIPE
for i in range(N):
	ctx[i] = {}
	proc = subprocess.Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=BUFSIZE)
	ctx[i]['proc'] = proc
	# metadata
	ctx[i]['pid'] = proc.pid
	ctx[i]['t_start'] = time()
	ctx[i]['head_cnt_in'] = 0
	ctx[i]['head_cnt_out'] = 0

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

from pprint import pprint
pprint(ctx)
