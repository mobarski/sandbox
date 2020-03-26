from itertools import islice

from model import HoracyModel

model = HoracyModel('model_100/').load()

for x in islice(model.dense,10):
	print(x)
