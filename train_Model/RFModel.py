import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, StratifiedKFold, KFold
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

csv_file_path = 'D:\\Desktop\\data\\EAC\\EACupdate.csv'
EAC_df = pd.read_csv(csv_file_path)
X = EAC_df.drop(columns=['uid', 'acc','class'])
Y = EAC_df['class']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
# declare parameters
param_grid = {
    'max_depth': [3,4],
    'min_child_weight': [1,2],
    'reg_lambda': [1,2],
    'gamma': [0.1,0.2],
    'learning_rate': [0.05, 0.1],
    'subsample': [0.5,0.6],
    'colsample_bytree': [0.5,0.6],
    'n_estimators': [50,55]
    # 'max_depth': [i for i in range(3, 10,2)],
    # 'min_child_weight': [i for i in range(1, 11,2)],
    # 'reg_lambda': [i for i in range(0, 6,2)],
    # 'gamma': [i / 10.0 for i in range(1, 11,2)],
    # 'learning_rate': [i / 100.0 for i in range(1, 31,6)],
    # 'subsample': [i / 10.0 for i in range(5, 11,2)],
    # 'colsample_bytree': [i / 10.0 for i in range(5, 11,2)],
    # 'n_estimators': [i for i in range(50, 200,30)]

}

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# 在训练集上拟合模型
rf_model.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = rf_model.predict(X_test)

# 使用SHAP解释模型
explainer = shap.TreeExplainer(rf_model, X_train)
shap_values = explainer(X_train)
shap.plots.bar(shap_values[:, :, 1],max_display=50)

# 计算准确率
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)