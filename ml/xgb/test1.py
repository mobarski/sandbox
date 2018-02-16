import xgboost as xgb
import numpy as np

# LOAD DATA
dtrain = xgb.DMatrix('test1-train.txt')
dtest  = xgb.DMatrix('test1-test.txt')

# TRAIN
options = {'silent':1}
iters = 20
bst = xgb.train(options, dtrain, iters, [(dtest,'test'),(dtrain,'train')])

# FEATURE IMPORTANCE
for x in ['weight','gain','cover']:
	print(x,bst.get_score('',x))

# SAVE MODEL
bst.save_model('test1.model')
bst.dump_model('test1.model.txt',with_stats=True)

# LOAD MODEL
bst = xgb.Booster()
bst.load_model('test1.model')

# PREDICT
pred = bst.predict(dtest)
print(pred)
