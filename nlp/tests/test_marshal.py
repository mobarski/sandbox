import marshal
import numpy as np

a = np.array([[1,2],[3,4]],dtype=np.uint8)
m = marshal.dumps(a)
print(len(m))
