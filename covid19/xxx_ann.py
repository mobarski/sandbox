import nmslib

dense = [
	[1,2,3],
	[1,2,2],
	[2,1,1],
	[3,2,1],
]

sparse = [
	[(1,1),(2,2)],
	[(2,2),(4,0)],
	[(1,2),(3,4)]
]

q_dense = [1,2,3]
q_sparse = [(4,1),(2,2)]

# SPARSE
ann = nmslib.init(method='hnsw', space='cosinesimil_sparse', data_type=nmslib.DataType.SPARSE_VECTOR)
ann.addDataPointBatch(sparse)
ann.createIndex()
i_list,d_list = ann.knnQuery(q_sparse)
for i,d in zip(i_list,d_list):
	print(i,d)
ann.saveIndex('xxx_sparse.bin',save_data=True)

# DENSE	
ann = nmslib.init(method='hnsw', space='cosinesimil')
ann.addDataPointBatch(dense)
ann.createIndex()
i_list,d_list = ann.knnQuery(q_dense)
for i,d in zip(i_list,d_list):
	print(i,d)
ann.saveIndex('xxx_dense.bin',save_data=True)

