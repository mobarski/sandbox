from time import time
import sys

def timed(fun):
	def wrapped(*args,**kwargs):
		t0 = time()
		out = fun(*args,**kwargs)
		print(f'{fun.__name__} done in {time()-t0:.02f} seconds',file=sys.stdout)
		return out
	return wrapped
