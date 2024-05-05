# import arcpy
import pandas as pd
import numpy as np
import math
import scipy.stats as stats
# df = pd.DataFrame()
# df['uid'] = 0
# index = 0
# arcpy.env.workspace = "D:\\Desktop\\data\\gis_osm_gd\\shanghai_1\\shanghai.gdb"
# # 使用 SearchCursor 读取表格文件
# with arcpy.da.SearchCursor('gis_osm', ["uid"]) as cursor:
#     # 遍历每一行记录
#     for row in cursor:
#         df.at[index, 'uid'] = row[0]
#         index = index + 1
#         if index % 5000 == 0:
#             print(f'当前{index}')
# del cursor
#
# # 计算列 'column_name' 的唯一值数量
# unique_values_count = df['uid'].nunique()
#
# print("唯一值数量：", unique_values_count)

# csv_file_path = "D:\\Desktop\\data\\EAC\\EAC2.csv"
# df = pd.read_csv(csv_file_path)
# # 使用cut函数将'acc'列的值分箱，并统计每个箱中的数量
# bins = [i / 20.0 for i in range(21)]  # 生成分箱的边界
# df['acc_bins'] = pd.cut(df['acc'], bins=bins)
# counts = df['acc_bins'].value_counts().sort_index()
#
# print("每隔0.05的数量：")
# print(counts)

# csv_file_path = "D:\\Desktop\\data\\EAC\\EAC2.csv"
# df1 = pd.read_csv(csv_file_path)
# csv_file_path = 'D:\\Desktop\\data\\EAC\\trueData\\mean_trueData2.csv'
# df2 = pd.read_csv(csv_file_path)
#
# # 获取 col1 大于 100 的所有行
# filtered_rows = df1[df1['Map_changes'] > 50000]
# print(filtered_rows)
# # # 然后从筛选后的结果中选择感兴趣的列（比如 col2）
# # selected_col = filtered_rows['uid']
#
# # 筛选出在 df2 中 count 大于 10 的 uid
# uids_greater_than_10 = df2[df2['count'] < 10]['uid']
#
# # 使用筛选出的 uid 在 df1 中进行条件索引
# result = filtered_rows[filtered_rows['uid'].isin(uids_greater_than_10)]
#
# # 输出结果
# print(result)

csv_file_path = "E:\\Download\\seeds\\seeds_dataset.txt"
df = pd.read_csv(csv_file_path,sep='\s+',header=None)
df.rename(columns={7:'class'},inplace=True)
print(df)