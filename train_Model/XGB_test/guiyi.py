import numpy as np
import pandas as pd

csv_file_path = 'D:\\Desktop\\data\\EAC\\EACupdate4.csv'
ECA_df = pd.read_csv(csv_file_path)
normalized_data = (ECA_df - ECA_df.min()) / (ECA_df.max() - ECA_df.min())

# 将归一化后的数据保存为 CSV 文件
normalized_data.to_csv('D:\\Desktop\\data\\EAC\\EACupdate5.csv', index=False)