import sys; sys.path.append('..')
from tsv import *

if __name__=="__main__":
	from time import time
	t0=time()
	itr = tsv_iter('../data/__all__.txt',encoding=None)
	f = frame_from_iter(itr,['col','id','text'])
	print(f['col'][0],f['id'][0],f['text'][0])
	print(time()-t0)
	
	f = frame_from_iter([['aa','111','Z'],['bb','222','Y'],['aa','333','X']],['col','id','text'])
	p = where(f,['col'],lambda col:col=='aa')
	f2 = filter_frame(f,p)
	print(f2)
	
	h = tsv_header('../data/bgg_db_1806.csv')
	rows = tsv_iter('../data/bgg_db_1806.csv',line_offset=1)