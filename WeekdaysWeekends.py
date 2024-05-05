import datetime
import pandas as pd
import sqlalchemy
import pymysql

engine = sqlalchemy.create_engine('mysql+pymysql://root:zxcvbnm,./@localhost:3306/osm')
sql_DistinctUid = '''
select distinct uid from a1_9999999 order by (uid+0) asc
'''
df_DistinctUid = pd.read_sql(sql_DistinctUid, engine)
df_DistinctUid['Weekdays'] = 999  # 唯一值id  91行
df_DistinctUid['Weekends'] = 999  # 唯一值id  91行

sql_UidCreated = '''
select uid,created from a1_9999999 order by (uid+0) asc ,created asc
'''
df_UidCreated = pd.read_sql(sql_UidCreated, engine)  # 1000行
index = 0
for idrow in range(0, 91):  # 91次循环
    wdNum = 0
    weNum = 0
    tmpDate = "2000"
    for i in range(0, 1000):
        if ((df_UidCreated.iloc[i, 0] == df_DistinctUid.iloc[idrow, 0])):
            if  (df_UidCreated.iloc[i, 1] != tmpDate):
                if((datetime.datetime.strptime(str(df_UidCreated.iloc[i, 1]), "%Y-%m-%dT%H:%M:%SZ")).weekday()<5):
                    wdNum += 1
                    tmpDate = df_UidCreated.iloc[i, 1]
                else:
                    weNum += 1
                    tmpDate = df_UidCreated.iloc[i, 1]
            if(i == 999):
                df_DistinctUid.iloc[idrow, 1] = wdNum
                df_DistinctUid.iloc[idrow, 2] = weNum
        elif (i >= index):  # id不匹配，且已经到下头的时候才结算
            index = i
            df_DistinctUid.iloc[idrow, 1] = wdNum
            df_DistinctUid.iloc[idrow, 2] = weNum
            break
df_DistinctUid.to_excel("D:/Desktop/data/WdWe.xlsx")
# print(df_DistinctUid)
# print(df_UidCreated)