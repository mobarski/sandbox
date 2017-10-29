N = 100000

from time import time
from multiprocessing.managers import BaseManager
class QueueManager(BaseManager): pass
QueueManager.register('get_queue')
m = QueueManager(address=('127.0.0.1', 50000), authkey='abracadabra')
m.connect()
queue = m.get_queue()
t0=time()
for i in range(N):
	queue.put(str(i))
print(N/(time()-t0))
