import unittest
from kcv_x1 import KCV

def pairs(text,dlm=' ',dlm2=':',cast=str):
	for row in text.split(dlm):
		cols = row.split(dlm2)
		yield cols[0],cast(cols[1])

class test_memory_kcv(unittest.TestCase):
	
	def setUp(self):
		pass
		#self.db = KCV()
		#self.db.set_items('k1',pairs('a:3 b:1 c:2 d:0 e:5 f:4'))
	
	### WRITE ###
	
	def test_set(self):
		db = KCV()
		db.set('k1','c1',42)
		db.set('k1','c2',4.2)
		db.set('k1','c3','fourty two')
		db.set('k1',1,'one')
		db.set(2,'c2','two')
		self.assertEqual(db.get('k1','c1'),42)
		self.assertEqual(db.get('k1','c2'),4.2)
		self.assertEqual(db.get('k1','c3'),'fourty two')
		self.assertEqual(db.get('k1','c4'),None)
		self.assertEqual(db.get('k1',1),'one')
		self.assertEqual(db.get(2,'c2'),'two')
	
	def test_set_items(self):
		db = KCV()
		db.set_items('k1',pairs('a:aa b:bb c:cc'))
		self.assertEqual(db.get('k1','a'),'aa')
		self.assertEqual(db.get('k1','b'),'bb')
		self.assertEqual(db.get('k1','c'),'cc')
	
	def test_incr(self):
		db = KCV()
		db.incr('k1','c1',2)
		self.assertEqual(db.get('k1','c1'),2,'incorrect INCR of new key new col')
		db.incr('k1','c1',3)
		self.assertEqual(db.get('k1','c1'),5,'incorrect INCR of existing key existing col')
		db.incr('k1','c1',-1)
		self.assertEqual(db.get('k1','c1'),4,'incorrect INCR with negative value')
	
	def test_incr_items(self):
		db = KCV()
		db.incr_items('k1',pairs('a:11 b:22 c:33',cast=int))
		self.assertEqual(db.get('k1','a'),11)
		self.assertEqual(db.get('k1','b'),22)
		self.assertEqual(db.get('k1','c'),33)
		db.incr_items('k1',pairs('a:1 b:2 c:3',cast=int))
		self.assertEqual(db.get('k1','a'),12)
		self.assertEqual(db.get('k1','b'),24)
		self.assertEqual(db.get('k1','c'),36)

	def test_delete(self):
		db = KCV()
		db.set('k1','c1',123)
		db.set('k1','c2',321)
		self.assertEqual(db.get('k1','c1'),123)
		self.assertEqual(db.get('k1','c2'),321)
		db.delete('k1','c1')
		self.assertEqual(db.get('k1','c1'),None)
		self.assertEqual(db.get('k1','c2'),321)
		db.delete('k1','c2')
		self.assertEqual(db.get('k1','c2'),None)

	def test_drop(self):
		db = KCV()
		db.set('k1','c1',1)
		db.set('k2','c2',2)
		db.set('k3','c3',3)
		self.assertEqual(db.get('k1','c1'),1)
		self.assertEqual(db.get('k2','c2'),2)
		self.assertEqual(db.get('k3','c3'),3)
		db.drop()
		db.create()
		self.assertEqual(db.get('k1','c1'),None)
		self.assertEqual(db.get('k2','c2'),None)
		self.assertEqual(db.get('k3','c3'),None)
	
	### READ ###
	
	def test_get(self):
		db = KCV()
		db.set('k1','c1',1)
		db.set('k1','c2',2)
		db.set('k2','c3',3)
		self.assertEqual(db.get('k1','c1'),1)
		self.assertEqual(db.get('k1','c2'),2)
		self.assertEqual(db.get('k2','c3'),3)
		self.assertEqual(db.get('k2','c4'),None)
		self.assertEqual(db.get('k1','xxx',123),123)
		self.assertEqual(db.get('xxx','zzz',123),123)

	def test_items(self):
		db = KCV()
		db.set('k1','c1',1)
		db.set('k1','c2',2)
		db.set('k1','c3',3)
		items = dict(db.items('k1'))
		self.assertEqual(len(items),3)
		self.assertEqual(items['c2'],2)
		self.assertEqual(items['c3'],3)
		self.assertEqual(items['c3'],3)

	def test_scan_items(self):
		db = KCV()
		db.set('k11','c11',1)
		db.set('k11','c12',2)
		db.set('k12','c11',3)
		db.set('k12','c12',4)
		k_items = dict(db.scan_items('k1*','c11',cast=dict))
		self.assertEqual(len(k_items),2)
		self.assertEqual('k11' in k_items,True)
		self.assertEqual('k12' in k_items,True)
		self.assertEqual(len(k_items['k11']),1)
		self.assertEqual(len(k_items['k12']),1)
		self.assertEqual(k_items['k11']['c11'],1)
		self.assertEqual(k_items['k12']['c11'],3)

	def test_scan(self):
		db = KCV()
		db.set('k11','c11',1)
		db.set('k11','c12',2)
		db.set('k12','c11',3)
		db.set('k12','c12',4)
		
		kcv = list(db.scan(order='kaca'))
		self.assertEqual(len(kcv),4)
		self.assertEqual(kcv[0],('k11','c11',1))
		self.assertEqual(kcv[1],('k11','c12',2))
		self.assertEqual(kcv[2],('k12','c11',3))
		self.assertEqual(kcv[3],('k12','c12',4))
		
		k = list(db.scan(mode='k',order='ka'))
		self.assertEqual(len(k),2)
		self.assertEqual(k[0],'k11')
		self.assertEqual(k[1],'k12')

	def test_scan_int(self):
		db = KCV()
		db.set(1,11,111)
		db.set(1,12,123)
		db.set(2,22,222)
		db.set(2,11,234)
		db.set(3,11,345)
		
		kcv = list(db.scan(k=1,order='kaca'))
		self.assertEqual(len(kcv),2)
		self.assertEqual(kcv[0],(1,11,111))
		self.assertEqual(kcv[1],(1,12,123))

		kcv = list(db.scan(kin=[1,3],cin=[11,12],order='kaca'))
		self.assertEqual(len(kcv),3)
		self.assertEqual(kcv[0],(1,11,111))
		self.assertEqual(kcv[1],(1,12,123))
		self.assertEqual(kcv[2],(3,11,345))
		

	def test_col_store(self):
		db = KCV()
		db.set_items('k1',pairs('a:aa b:bb c:cc'))
		db.set_items('k2',pairs('d:dd e:ee f:ff'))
		db.set_items('k3',pairs('g:gg h:hh i:ii'))
		db.to_col_store('kcv_x1_test.db',batch=4)
		self.assertEqual(db.get('k1','a'),'aa')
		self.assertEqual(db.get('k2','e'),'ee')
		self.assertEqual(db.get('k3','i'),'ii')
		db.drop()
		db.create()
		self.assertEqual(db.items('k1'), {})
		self.assertEqual(db.items('k2'), {})
		self.assertEqual(db.items('k3'), {})
		db.from_col_store('kcv_x1_test.db')
		self.assertEqual(db.get('k1','a'),'aa')
		self.assertEqual(db.get('k2','e'),'ee')
		self.assertEqual(db.get('k3','i'),'ii')

	def test_block(self):
		with KCV('kcv_x1_test.db') as db:
			db.set('k1','c1',42)
		db2=KCV('kcv_x1_test.db')
		self.assertEqual(db2.get('k1','c1'),42)
	
	def test_compact(self):
		import os
		path = 'kcv_x1_test.db'
		db=KCV(path)
		for i in range(1000):
			db.set(i,i,i)
		db.sync()
		size1 = os.stat(path)[6]
		db.drop()
		db.sync()
		size2 = os.stat(path)[6]
		db.sync(compact=True)
		size3 = os.stat(path)[6]
		self.assertTrue(size3 < size2 <= size1)


if __name__=="__main__":
	unittest.main()
