import marshal
import sys
import os

ROOT = '../data/cache'

# KEY-VALUE INTERFACE

# TODO rename col,key1,key2 -> db,col,key ??? col,msr,key ??? col,key,agg/level

def get(col,key1,key2,default=None):
	path = _path(col,key1,key2)
	try:
		with open(path,'rb') as f:
			data = marshal.load(f)
			return data
	except:
		return default

def set(col,key1,key2,value):
	path = _path(col,key1,key2)
	if value is not None:
		f = open(path,'wb')
		marshal.dump(value,f)
	else:
		if os.path.exists(path):
			os.remove(path)

def delete(col,prefix):
	col_dir = os.path.join(ROOT,col)
	rm_cnt = 0
	for key1 in os.listdir(col_dir):
		key_dir = os.path.join(col_dir,key1)
		for key2 in os.listdir(key_dir):
			if key2.startswith(prefix):
				path = os.path.join(key_dir,key2)
				os.remove(path)
				rm_cnt += 1
	return rm_cnt

# HELPERS: KEY-VALUE

def _path(col,key1,key2):
	dir = os.path.join(ROOT,col,key1)
	if not os.path.exists(dir):
		os.makedirs(dir)
	path = os.path.join(dir,key2)
	return path

# TODO list_all powinno byc publiczne
def _list_all(col, key1):
	path = _path(col,key1,'')
	return os.listdir(path)

# ------------------------------------------------------------------------------

# RANGE INTERFACE

def get_range(col, key1, key2_from, key2_to, inclusive=True):
	all = _list_all(col,key1)
	top = _limit_top(_limit_range(all, key2_from, key2_to, inclusive))
	data = [get(col,key1,k) for k in top]
	return data,top	

# TODO invalidate

# HELPERS: RANGE

def _limit_range(all, k_from, k_to=None, inclusive=True):
	if k_to:
		if inclusive:
			out = [k for k in all if k>=k_from and (k<k_to or k.startswith(k_to))]
		else:
			out = [k for k in all if k>=k_from and k<k_to]
	else:
		# TODO k_from is not string (list / tuple / set)
		out = [k for k in all if k.startswith(k_from)]
	out.sort()
	return out

def _limit_top(k_list):
	if not k_list: return []
	curr = k_list[0]
	out = [curr]
	for k in k_list[1:]:
		if k.startswith(curr):
			pass
		else:
			out += [k]
			curr = k
	return out

# ------------------------------------------------------------------------------

if __name__=="__main__":
	COL = 'test'
	set(COL,'k1','k2',None)
	set(COL,'k1','k21',[1])
	set(COL,'k1','k22',[2])
	set(COL,'k1','k23',[3])
	set(COL,'k1','k3',[3,4,5])
	set(COL,'k1','k34',[3,4])
	set(COL,'k1','k35',[3,5])
	set(COL,'k1','k4',[4,5,6])
	set(COL,'k1','k',[1,2,3,4,5,6])
	v = get(COL,'k1','k3')
	print(v)
	all = _list_all(COL,'k1')
	print('list_all',all)
	r = _limit_range(all,'k1','k4',inclusive=True)
	print('range',r)
	print('top',_limit_top(r))
	print('get_range',get_range(COL,'k1','k2','k4'))

	