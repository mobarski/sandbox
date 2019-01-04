from __future__ import print_function
import sys; sys.path.append('contrib')
import traceback as tb
import inspect
import marshal
import pickle
import os
from random import randint

"""
Distant - RPC over SSH with Public Key Authentication
version: 2019-01-04
"""

# TODO rename contrib ??? -> site_pkg -> site_repo -> pkg_repo -> repo

# ---[ API LAYER ]--------------------------------------------------------------

def setup(host, cfg={}, verbose=True):
	return call(host, None, None, cfg=cfg, verbose=verbose, setup=True)

def call(host, fun, data, cfg={}, verbose=False, setup=False):
	"""Call fun(data) on remote host and return the results or raise the exception"""
	ssh = cfg_get(cfg, 'ssh', 'ssh', host=host)
	rsync = cfg_get(cfg, 'rsync', 'rsync -vr', host=host)
	full_host = cfg_get_host(cfg, host)	
	remote_contrib = cfg_get(cfg, 'remote_contrib')
	local_contrib = cfg.get('local_contrib')
	work = cfg.get('work')

	if fun:
		assert fun.__name__ != '<lambda>'
		name = str(time()).replace('.','_')
		path = '{}/{}_{}_{}.job'.format(work,host,name,randint(100000,999999))
		save_job(path, fun, data)
	else:
		path = None
	
	return remote_run(path, full_host,
		ssh=ssh, rsync=rsync,
		remote_contrib=remote_contrib,
		local_contrib=local_contrib,
		verbose=verbose, setup=setup)

# ---[ INTERNAL LAYER ]---------------------------------------------------------

def remote_run(path, host,
		ssh, rsync,
		remote_contrib=None,
		local_contrib=None,
		verbose=False,
		setup=False,
		remove_local_files=True):
	""""""	
	assert remote_contrib
	assert ssh
	assert host
	
	# init host
	if setup:
		assert local_contrib
		assert rsync
		cmd = ssh+' '+host+' mkdir -p '+remote_contrib
		run_cmd(cmd, verbose=verbose)
		remote_contrib_parent = remote_contrib.rsplit('/',2 if remote_contrib.endswith('/') else 1)[0]
		cmd = rsync+' '+local_contrib+' '+host+':'+remote_contrib_parent
		run_cmd(cmd, verbose=verbose)
	
	# empty job - just for init host
	if not path: return None
	
	# run job
	out_path = path[:-3]+'out'
	with open(path,'r') as fi:
		with open(out_path,'w') as fo:
			cmd = ssh+' '+host+" PYTHONPATH={} python -m distant run2".format(remote_contrib)
			run_cmd(cmd, stdin=fi, stdout=fo, verbose=False)

	# load output
	with open(out_path,'r') as f:		
		result = marshal.load(f)
		exc = marshal.load(f)

	# remove local files
	if remove_local_files:
		os.remove(path)
		os.remove(out_path)

	if exc:
		print(exc)
		raise Exception('RemoteError')
	else:
		return result

# ---[ CORE LAYER ]-------------------------------------------------------------

m_ver = 0 # marshal version
p_ver = 0 # pickle version

def save_job(path, fun, data, meta={}):
	"""Store job (function + data + metadata) in a file"""
	if not meta: meta={}
	
	with open(path,'wb') as f:
		# meta
		pickle.dump(meta, f, p_ver)
		# function
		if True:
			# omit problems with pickle.dump(fun, f)
			src = '\n' * (fun.__code__.co_firstlineno - 1) # preserve line numbers
			src += inspect.getsource(fun)
			pickle.dump((
							fun.__name__,
							src,
							fun.__code__.co_filename
				), f, p_ver)
		# data
		marshal.dump(data, f, m_ver)

def run(path):
	"""Run job from input file and store results in output file"""
	out_path = path[:-3]+'out'
	with open(path,'rb') as fi:
		with open(out_path,'wb') as fo:
			out = _run(fi, fo)
	return out

def run2():
	"""Run job from stdin and store results in stdout"""
	return _run(sys.stdin, sys.stdout)

def _run(fi,fo):
	# load
	f = fi
	meta = pickle.load(f) # TODO globals ???
	if 0:
		fun = pickle.load(f)
	else:
		name,src,co_filename = pickle.load(f)
		code = compile(src,co_filename,'exec')
		exec(code)
		fun = locals()[name]
	data = marshal.load(f)
	
	# call
	try:
		result = fun(data)
		exc = ''
	except Exception as e:
		result = None
		exc = tb.format_exc()
	
	# output
	f = fo
	marshal.dump(result, f, m_ver)
	marshal.dump(exc,    f, m_ver)
	
	return result,exc

# ---[ UTILS ]------------------------------------------------------------------

import subprocess as sp
from time import time

# TODO cleanup the code
def run_cmd(cmd,stdin=None,stdout=None,stderr=None,verbose=True, shell=True):
	if verbose:
		t0 = time()
		print('CMD:',cmd)
		sys.stdout.flush()
		p = sp.Popen(cmd,stdin=stdin,shell=shell)
		print('PID:',p.pid,'\n')
		sys.stdout.flush()
		rc = p.wait()
		if rc:
			sys.stdout.flush()
			sys.stderr.flush()
			raise Exception('RC != 0')
		print('TIME: {:.2f}s'.format(time()-t0))
		print()	
	elif stdout is None:
		p = sp.Popen(cmd, stdin=stdin, stdout=sp.PIPE, stderr=sp.PIPE, shell=shell)
		out,err = p.communicate()
		rc = p.returncode
		if rc:
			print(err)
			raise Exception('RC != 0')
	else:
		print('CMD:',cmd)
		p = sp.Popen(cmd, stdin=stdin, stdout=stdout, stderr=sp.PIPE, shell=shell)
		out,err = p.communicate()
		rc = p.returncode
		if rc:
			print(err)
			raise Exception('RC != 0')

def cfg_get(cfg, key, default=None, host=None):
	if key+'_host' in cfg and host in cfg[key+'_host']:
		return cfg[key+'_host'][host]
	else:
		return cfg.get(key,default)

def cfg_get_host(cfg, host):
	if 'host' in cfg:
		return cfg['host'].get(host,host)
	else:
		return host

# ------------------------------------------------------------------------------

if __name__=="__main__":
	mode = sys.argv[1]
	if mode == 'run':
		path = sys.argv[2]
		out = run(path)
		print(out)
	else:
		run2()
