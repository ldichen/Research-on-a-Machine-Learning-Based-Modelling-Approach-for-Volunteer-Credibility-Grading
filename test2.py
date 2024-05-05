
import pandas as pd
# 读取CSV文件
df = pd.read_csv("D:\\Desktop\\data\\140000001_150000000(不完整)\\38000001_110000000.csv",encoding='utf-8')

# 提取前五列
first_five_columns = df.iloc[:, :4]

# 提取最后 10 行数据
last_ten_rows = first_five_columns.tail(10)

print(last_ten_rows)