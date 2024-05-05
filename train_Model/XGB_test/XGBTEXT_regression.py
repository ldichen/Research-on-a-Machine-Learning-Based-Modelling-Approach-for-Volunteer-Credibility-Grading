import pandas
import pandas as pd
import xgboost as xgb
import numpy as np

data = pd.read_excel('./Concrete_Data.xls')

data.rename(columns={"Concrete compressive strength(MPa, megapascals) ": 'label'}, inplace=True)
# print(data.head(10))
mask = np.random.rand(len(data)) < 0.8
train = data[mask]
test = data[~mask]

xgb_train = xgb.DMatrix(train.iloc[:, :7], label=train.label)
xgb_test = xgb.DMatrix(test.iloc[:, :7], label=test.label)

params = {
    'objective': 'reg:linear',
    'booster': 'gbtree',
    'eta': 0.1,
    'max_depth': 5,
    'min_child_weight': 1,
}

watchlist = [(xgb_train, 'train'), (xgb_test, 'test')]
num_round = 50
model = xgb.train(params, xgb_train, num_round, evals=watchlist)
model.save_model('./model.json')

bst =xgb.Booster()
bst.load_model('./model.json')
print(test)
pred = bst.predict(xgb_test)
print(pred)