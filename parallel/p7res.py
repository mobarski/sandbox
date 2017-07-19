## p7res.py - p7 resource reservation
## (c) 2017 by mobarski (at) gmail (dot) com
## licence: MIT
## version: x1

# cmd-api: pid label res-amount res-name1 res-name2 res-name3 
# >>> p7res.py 12345 streamy_20170717 RAM,SDD,HDD:10
# /dev/shm/logi_vsender

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
import time
import pickle

LOCK_FILE_NAME = 'p7res.lock'
FLAGS = os.O_CREAT | os.O_EXCL

try:
	fd = os.open(LOCK_FILE_NAME,FLAGS)
	os.close(fd)
except: # OSError / FileExistsError
	print('FILE EXISTS')



os.remove(LOCK_FILE_NAME)