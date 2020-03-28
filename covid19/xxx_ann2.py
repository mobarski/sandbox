import nmslib
import numpy as np
from random import shuffle,randint
from time import time

# DENSE 

if 0:
	a = np.random.rand(50000,50)
	print(a)

	t1=time()
	ann = nmslib.init(method='hnsw', space='cosinesimil')
	if 0:
		ann.loadIndex('xxx_dense.bin',load_data=True)
	else:
		ann.addDataPointBatch(a)
		ann.createIndex()
		ann.saveIndex('xxx_dense.bin',save_data=True)
	i_list,d_list = ann.knnQuery([0.5]*50)
	for i,d in zip(i_list,d_list):
		print(i,d)
	print(dir(ann))
	print(ann[1])
	print(f"t1: {time()-t1:.02f} seconds")

# SPARSE

if 1:
	# 50k -> 7s
	t0 = time()
	sparse = []
	for i in range(500):
		d = {}
		for i in range(50):
			x = randint(1,100000)
			if x in d:
				d[x] += 1
			else:
				d[x] = 1
		sparse += [tuple(d.items())]
	print(f"t0: {time()-t0:.02f} seconds")
	print(sparse[:2])

	# 50k -> 120s
	t1 = time()
	ann = nmslib.init(method='hnsw', space='cosinesimil_sparse', data_type=nmslib.DataType.SPARSE_VECTOR)
	ann.addDataPointBatch(sparse)
	ann.createIndex()
	ann.saveIndex('xxx_sparse.bin',save_data=True)
	print(f"t1: {time()-t1:.02f} seconds")
