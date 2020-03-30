import nmslib
from tqdm import tqdm

from util_time import timed

class HoracyANN():

	@timed
	def init_dense_ann(self):
		self.dense_ann = nmslib.init(method='hnsw', space='cosinesimil')
		dense = self.dense
		dense = tqdm(dense, desc='ann_input')
		for i,point in enumerate(dense):
			self.dense_ann.addDataPoint(i,[x[1] for x in point])
		self.dense_ann.createIndex(print_progress=True)
		self.dense_ann.saveIndex(self.path+'ann_dense.bin',save_data=True)

	@timed
	def init_sparse_ann(self):
		self.sparse_ann = nmslib.init(method='hnsw', space='cosinesimil_sparse', data_type=nmslib.DataType.SPARSE_VECTOR)
		sparse = self.sparse
		sparse = tqdm(sparse, desc='ann_input')
		for i,point in enumerate(sparse):
			self.sparse_ann.addDataPoint(i,point)		
		self.sparse_ann.createIndex(print_progress=True)
		self.sparse_ann.saveIndex(self.path+'ann_sparse.bin',save_data=True)

	def load_dense_ann(self):
		self.dense_ann = nmslib.init(method='hnsw', space='cosinesimil')
		self.dense_ann.loadIndex(self.path+'ann_dense.bin',load_data=True)

	def load_sparse_ann(self):
		self.sparse_ann = nmslib.init(method='hnsw', space='cosinesimil_sparse', data_type=nmslib.DataType.SPARSE_VECTOR)
		self.sparse_ann.loadIndex(self.path+'ann_sparse.bin',load_data=True)

	def sparse_ann_query(self, point, k=10):
		return self.sparse_ann.knnQuery(point, k)

	def dense_ann_query(self, point, k=10):
		return self.dense_ann.knnQuery(point, k)
