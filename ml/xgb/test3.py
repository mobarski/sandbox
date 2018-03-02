import xgboost as xgb

data = [[1,0],[4,0],[0,1],[0,4],[3,1],[1,3]]
labels = [1,1,0,0,1,0]

dtrain = xgb.DMatrix(data,label=labels)

param = {}
#param['objective'] = 'multi:softmax'
param['objective'] = 'multi:softprob'
param['num_class'] = 2
#param['eval_metric'] = 'mlogloss'
model = xgb.train(param,dtrain,200,evals=[[dtrain,'train']])

pred = model.predict(xgb.DMatrix([[0,1],[1,0],[0,2],[2,0]]))
print(pred)
