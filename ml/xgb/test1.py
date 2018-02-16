import xgboost as xgb
import numpy as np

dtrain = xgb.DMatrix('test1-train.txt')
dtest  = xgb.DMatrix('test1-test.txt')

options = {'silent':1}
iters = 20
bst = xgb.train(options, dtrain, iters, [(dtest,'test'),(dtrain,'train')])

for x in ['weight','gain','cover']:
	print(x,bst.get_score('',x))

bst.save_model('test1.model')
bst.dump_model('test1.model.txt',with_stats=True)
