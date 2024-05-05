import datetime
import pandas as pd
import sqlalchemy
from tqdm import tqdm
from multiprocessing import cpu_count, Pool
import pymysql
import gc

'''
------------------------------------------------------插入数据库连接------------------------------------------------------
'''
db = pymysql.Connect(
    host='localhost',
    user='root',
    password='zxcvbnm,./',
    database='osm',
    port=3306,
    charset='utf8',
    autocommit=True
)
'''
-----------------------------------------------id，编辑天数，工作日次数，周末次数--------------------------------------------
'''


def EditDays(uid):
    # engine = sqlalchemy.create_engine('mysql+pymysql://root:zxcvbnm,./@localhost:3306/osm')
    uid['EditDays'] = 2.0
    uid['Weekdays'] = 999
    uid['Weekends'] = 999
    sql_UidCreated = f'''
    select uid,created from test10000 order by (uid+0) asc ,created asc
    '''
    df_UidCreated = pd.read_sql(sql_UidCreated, engine)  # 1000行

    index = 0
    print("-------------天数数据处理中---------------")
    for idrow in tqdm(range(0, len(uid))):
        ft = df_UidCreated.iloc[index, 1]
        wdNum = 0
        weNum = 0
        EditDays = 0.0
        for i in range(index, len(df_UidCreated)):
            if (df_UidCreated.iloc[i, 0] == uid.iloc[idrow, 0]):
                lt = df_UidCreated.iloc[i, 1]
                # if (df_UidCreated.iloc[i, 1] != tmpDate):
                # 是同一天
                if (datetime.datetime.strptime(str(lt), "%Y-%m-%dT%H:%M:%SZ").date() == datetime.datetime.strptime(
                        str(ft), "%Y-%m-%dT%H:%M:%SZ").date()):
                    EditDays = EditDays + (
                            datetime.datetime.strptime(str(lt), "%Y-%m-%dT%H:%M:%SZ") - datetime.datetime.strptime(
                        str(ft), "%Y-%m-%dT%H:%M:%SZ")).seconds / 3600
                    if (EditDays == 0.0):
                        EditDays = EditDays + 1
                    if ((
                            datetime.datetime.strptime(str(df_UidCreated.iloc[i, 1]),
                                                       "%Y-%m-%dT%H:%M:%SZ")).weekday() < 5):
                        wdNum += 1
                    else:
                        weNum += 1
                # 不是同一天
                else:
                    EditDays = EditDays + 1
                    if ((
                            datetime.datetime.strptime(str(df_UidCreated.iloc[i, 1]),
                                                       "%Y-%m-%dT%H:%M:%SZ")).weekday() < 5):
                        wdNum += 1
                    else:
                        weNum += 1
                ft = df_UidCreated.iloc[i, 1]
                if (i == len(df_UidCreated) - 1):
                    uid.iloc[idrow, 1] = EditDays
                    uid.iloc[idrow, 2] = wdNum
                    uid.iloc[idrow, 3] = weNum
            else:  # id不匹配
                index = i
                uid.iloc[idrow, 1] = EditDays
                uid.iloc[idrow, 2] = wdNum
                uid.iloc[idrow, 3] = weNum
                break
    return uid
    # df_DistinctUid.loc[df_DistinctUid['EditDays'] == 0.0, 'EditDays'] = 0.08  # 处理一下零值
    # df_DistinctUid.to_excel(f"D:/Desktop/data/EditDaystest.xlsx")


'''
-----------------------------------------------编辑节点数，节点更改数和评论次数----------------------------------------------
'''


def editNode(uid):
    uid['NodeNum'] = 999
    uid['NumChanges'] = 999999
    uid['Comments_Count'] = 999999
    sql_DistinctCreated = '''
    select distinct created,uid,num_changes,comments_count from test10000 order by (uid+0) asc ,created asc
    '''
    df_DistinctCreated = pd.read_sql(sql_DistinctCreated, engine)
    # df_DistinctCreated.to_excel("D:/Desktop/data/Numtest.xlsx")
    df_DistinctCreated['num_changes'] = df_DistinctCreated['num_changes'].astype(int)
    df_DistinctCreated['comments_count'] = df_DistinctCreated['comments_count'].astype(int)
    allSum = df_DistinctCreated.groupby('uid').sum()
    # print(allSum)
    allNum = df_DistinctCreated['uid'].value_counts()
    # print(allNum)
    print("-------------节点数据处理中---------------")
    for idrow in tqdm(range(0, len(uid))):
        uid.iloc[idrow, 1] = allNum[str(uid.iloc[idrow, 0])]
        uid.iloc[idrow, 2] = allSum.loc[str(uid.iloc[idrow, 0]), 'num_changes']
        uid.iloc[idrow, 3] = allSum.loc[str(uid.iloc[idrow, 0]), 'comments_count']
    print("-------------数据处理已完成，准备数据导入---------------")
    # uid.to_excel("D:/Desktop/data/ NodeNum_Changes_comments.xlsx")
    return uid


'''
------------------------------------ ------------------执行数据库插入------------------------------------------------------
'''


def insertSQl(begin, end, editResult):
    insersql = 'INSERT INTO volunteer(uid,EditDays,Weekdays,Weekends,NodeNum,NumChanges,Comments_Count) VALUES'
    for i in tqdm(range(begin, end)):  # python进度条 tqdm
        k = i + 1
        if k % 1000 == 0:  # 每10000次进行一次插入，速度没有经过校验，不确定10000万次是否为最佳
            insersql = insersql.strip(',\n')  # sql语句拼接时最后会留下一个逗号，不删除会报错
            try:
                db.ping(reconnect=True)  # reconnect 自动重联
                cur = db.cursor()
                cur.execute(insersql)
                db.commit()
                cur.close()
                db.close()
                del insersql  # 删除变量
                gc.collect()  # 回收内存空间

            except Exception as e:
                print(e)
            # sql重置
            insersql = 'INSERT INTO volunteer(uid,EditDays,Weekdays,Weekends,NodeNum,NumChanges,Comments_Count) VALUES'
        insersql += f"('{editResult.iloc[i, 0]}','{editResult.iloc[i, 1]}','{editResult.iloc[i, 2]}','{editResult.iloc[i, 3]}','{editResult.iloc[i, 4]}','{editResult.iloc[i, 5]}','{editResult.iloc[i, 6]}'),"


'''
--------------------------------------------总流程：读取原始数据，预处理以及多进程插入-----------------------------------------
'''
if __name__ == '__main__':
    startTime = datetime.datetime.now()
    print("-------------读取数据中---------------")
    engine = sqlalchemy.create_engine('mysql+pymysql://root:zxcvbnm,./@localhost:3306/osm')
    sql_DistinctUid = f'''
    select distinct uid from test10000 order by (uid+0) asc
    '''
    df_DistinctUid = pd.read_sql(sql_DistinctUid, engine)
    Copy_DistinctUid = df_DistinctUid.copy()
    print("-------------基础数据读取完成，天数数据读取中---------------")
    editResult01 = EditDays(df_DistinctUid)

    print("-------------天数数据处理完成，节点数据读取中---------------")
    editResult02 = editNode(Copy_DistinctUid)

    print("----------------------数据合并中------------------------")
    editResult = pd.merge(editResult01, editResult02, on='uid')

    p = Pool(5)  # cpu_count 查询当前设备进程数
    print("-----------------数据合并完成，数据插入中------------------")
    for i in range(5):
        begin = i * 2000
        end = (i + 1) * 2000
        p.apply_async(insertSQl, args=[begin, end, editResult])
    p.close()
    p.join()
    endTime0 = datetime.datetime.now()
    print("已完成", endTime0 - startTime)
