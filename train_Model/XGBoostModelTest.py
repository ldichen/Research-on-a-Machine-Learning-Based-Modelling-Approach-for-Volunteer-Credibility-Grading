import shap
import xgboost as xgb
from xgboost import XGBClassifier
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split

csv_file_path = "E:\\Download\\seeds\\seeds_dataset.txt"
df = pd.read_csv(csv_file_path, sep='\s+', header=None, converters={7: lambda x: int(x) - 1})
df.rename(columns={0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: 'class'}, inplace=True)

X = df.drop(columns=['class'])
Y = df['class']
# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

xgb_model = XGBClassifier(random_state=42,num_class = 3,objective='multi:softmax',learning_rate=0.01)
xgb_model.fit(X_train, y_train)

# xgb.plot_importance(xgb_model)

# SHAP计算
explainer = shap.TreeExplainer(xgb_model,X_train)
shap_values = explainer(X_train)
shap.plots.bar(shap_values[:, :, 1])
# shap.plots.bar(shap_values[:, :, 1])
# shap.summary_plot(shap_values[:, :, 1], X_train)
