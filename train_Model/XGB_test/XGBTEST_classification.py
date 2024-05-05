import pandas as pd
import xgboost as xgb
import numpy as np

# read dataset
data = pd.read_csv('seeds_dataset.txt', header=None, sep='\s+', converters={7: lambda x: int(x) - 1})
# rename label
data.rename(columns={7: 'label'}, inplace=True)

# print(data.head(10))

# bool array
mask = np.random.rand(len(data)) < 0.8
train = data[mask]
test = data[~mask]

xgb_train = xgb.DMatrix(train.iloc[:, :6], label=train.label)
xgb_test = xgb.DMatrix(test.iloc[:, :6], label=test.label)

# softmax Direct classification
# softprob probability vector
params = {
    'objective': 'multi:softprob',
    'eta': 0.1,
    'max_depth': 5,
    'num_class': 3,
    'eval_metric': 'merror'
}

watchlist = [(xgb_train, 'train'), (xgb_test, 'test')]

num_round = 50
bst = xgb.train(params, xgb_train, num_round, evals=watchlist)
pred = bst.predict(xgb_test)
print(pred)
error_rate = np.sum(pred != test.label) / test.shape[0]
print(f'test error rate :{error_rate}')