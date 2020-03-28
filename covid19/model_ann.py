import nmslib
from tqdm import tqdm

from util_time import timed

class HoracyANN():

	@timed
	def init_ann_dense(self):
		self.ann = nmslib.init(method='hnsw', space='cosinesimil')
		dense = self.dense
		dense = tqdm(dense, desc='ann_input')
		for i,point in enumerate(dense):
			self.ann.addDataPoint(i,[x[1] for x in point])
		self.ann.createIndex(print_progress=True)
		self.ann.saveIndex(self.path+'ann.bin',save_data=True)

	@timed
	def init_ann_sparse(self):
		self.ann = nmslib.init(method='hnsw', space='cosinesimil_sparse', data_type=nmslib.DataType.SPARSE_VECTOR)
		sparse = self.sparse
		sparse = tqdm(sparse, desc='ann_input')
		for i,point in enumerate(sparse):
			self.ann.addDataPoint(i,point)		
		self.ann.createIndex(print_progress=True)
		self.ann.saveIndex(self.path+'ann.bin',save_data=True)

	def load_ann_dense(self):
		self.ann = nmslib.init(method='hnsw', space='cosinesimil')
		self.ann.loadIndex(self.path+'ann.bin',load_data=True)

	def load_ann_sparse(self):
		self.ann = nmslib.init(method='hnsw', space='cosinesimil_sparse', data_type=nmslib.DataType.SPARSE_VECTOR)
		self.ann.loadIndex(self.path+'ann.bin',load_data=True)

	def ann_query(self, point, k=10):
		return self.ann.knnQuery(point, k)
		