## p7res.py - p7 resource reservation
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: x1

# cmd-api: pid label res-amount res-name1 res-name2 res-name3 
# >>> p7res.py 12345 streamy_20170717 RAM,SDD,HDD:10
# /dev/shm/logi_vsender

# x1 - zasoby: efekt wykonania polecenia np. df+grep

# TODO rename: p7lock p7rm p7man 

# lock or die on timeout
# read config
# check reservations
# kill old reservations
# check resources
# create reservation
# ouput -> one line per resource? env-variables?
# unlock
# end

import os
import sys
import time
import pickle
import subprocess
import json
from pprint import pprint

DEBUG = True
LOCK_FILE_NAME = 'p7res.lock'
CONF_FILE_NAME = 'p7res.cfg'
STATE_FILE_NAME = 'p7res.state'
FLAGS = os.O_CREAT | os.O_EXCL

cfg = {} # resource name -> configuration dict
resource = {} # name -> resource state (free, reserved)
state = {} # name -> list of reservations

def log(text=None,data=None):
	if DEBUG:
		if text!=None: print(text,file=sys.stderr)
		if data!=None: pprint(data,stream=sys.stderr)

def pid_is_running(pid):
	try:
		os.kill(pid, 0)
	except OSError:
		return False
	else:
		return True


def lock_or_die_on_timeout():
	# TODO
	try:
		fd = os.open(LOCK_FILE_NAME,FLAGS)
		os.close(fd)
	except: # OSError / FileExistsError
		print('FILE EXISTS')
		sys.exit(1)


def read_config():
	global cfg
	f = open(CONF_FILE_NAME,'r')
	cfg = json.load(f)
	if DEBUG:
		log('CONFIG:',cfg)
		log('')


def init_resources():
	for name,res_cfg in cfg.items():
		resource[name] = dict(reserved=0) # TODO


def kill_old_reservations():
	# mark
	for res_name,res_list in state.items():
		for reservation in res_list:
			pid = reservation['pid']
			is_old = time.time() > reservation['deadline']
			if is_old:
				log('old reservation of %s by pid %s (deadline)' % (res_name,pid))
			if not pid_is_running(pid):
				log('old reservation of %s by pid %s (no such pid)' % (res_name,pid))
				is_old = True
			reservation['old'] = is_old
	# sweep
	for res_name,res_list in state.items():
		state[res_name] = [r for r in res_list if not r['old']]


def make_reservation(pid, res_name, amount=1, timeout=1.0):
	if res_name not in state:
		state[res_name] = []
	t = time.time() + timeout*60*60
	reservation = dict(pid=pid, res_name=res_name, amount=amount, deadline=t)
	state[res_name].append(reservation)


def cancel_reservation(pid, res_name):
	if res_name not in state: pass # TODO
	idx = None
	for i,reservation in enumerate(state['res_name'].values()):
		if reservation['pid']==pid:
			idx = i
			break
	if idx != None:
		del state['res_name'][idx]


def read_reservations():
	global state
	try:
		f = open(STATE_FILE_NAME,'r')
		state = json.load(f)
		f.close()
	except: # TODO
		state = {}


def check_resources():
	# wykonanie polecen zwracajacych ilosc zasobu
	for name,res_cfg in cfg.items():
		if 'cmd' in res_cfg:
			cmd = res_cfg['cmd']
			# TODO errorhandling
			#out = subprocess.check_output(cmd, shell=True)
			out = '123'
			resource[name]['avail'] = int(out)


def create_reservation():
	make_reservation(1234,'MB_HDD_REMOTE',1,0.0001) # TODO FIX HARDCODE


def ouput_reservation():
	if DEBUG:
		log('\nRESOURCES:',resource)
		log('')

def save_reservations():
	f = open(STATE_FILE_NAME,'w')
	json.dump(state,f)
	f.close()

def unlock():
	os.remove(LOCK_FILE_NAME)


#-------------------------------------------------------------------


def main():
	lock_or_die_on_timeout()
	read_config()
	read_reservations()
	kill_old_reservations()
	init_resources()
	check_resources()
	create_reservation()
	save_reservations()
	ouput_reservation()
	unlock()


if __name__=="__main__":
	main()
