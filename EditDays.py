import datetime
import pandas as pd
import sqlalchemy
from tqdm import tqdm
from multiprocessing import cpu_count, Pool
import pymysql
import gc

db = pymysql.Connect(
    host='localhost',
    user='root',
    password='zxcvbnm,./',
    database='osm',
    port=3306,
    charset='utf8',
    autocommit=True
)

def EditDays():
    sql_UidCreated = f'''
    select uid,created from test10000 order by (uid+0) asc ,created asc
    '''
    df_UidCreated = pd.read_sql(sql_UidCreated, engine)  # 1000行

    index = 0

    for idrow in range(0, len(df_DistinctUid)):
        ft = df_UidCreated.iloc[index, 1]
        wdNum = 0
        weNum = 0
        EditDays = 0.0
        for i in range(index, len(df_UidCreated)):
            if (df_UidCreated.iloc[i, 0] == df_DistinctUid.iloc[idrow, 0]):
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
                    df_DistinctUid.iloc[idrow, 1] = EditDays
                    df_DistinctUid.iloc[idrow, 2] = wdNum
                    df_DistinctUid.iloc[idrow, 3] = weNum
            else:  # id不匹配
                index = i
                df_DistinctUid.iloc[idrow, 1] = EditDays
                df_DistinctUid.iloc[idrow, 2] = wdNum
                df_DistinctUid.iloc[idrow, 3] = weNum
                break
    print('edit结束')
    return df_DistinctUid
    # df_DistinctUid.loc[df_DistinctUid['EditDays'] == 0.0, 'EditDays'] = 0.08  # 处理一下零值
    # df_DistinctUid.to_excel(f"D:/Desktop/data/EditDaystest.xlsx")


def insertSQl(begin, end, editResult):
    insersql = 'INSERT INTO volunteer(uid,EditDays,Weekdays,Weekends) VALUES'
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
            insersql = 'INSERT INTO volunteer(uid,EditDays,Weekdays,Weekends) VALUES'
        insersql += f"('{editResult.iloc[i, 0]}','{editResult.iloc[i, 1]}','{editResult.iloc[i, 2]}','{editResult.iloc[i, 3]}'),"


if __name__ == '__main__':
    startTime = datetime.datetime.now()
    engine = sqlalchemy.create_engine('mysql+pymysql://root:zxcvbnm,./@localhost:3306/osm')
    sql_DistinctUid = f'''
    select distinct uid from test10000 order by (uid+0) asc
    '''
    df_DistinctUid = pd.read_sql(sql_DistinctUid, engine)
    df_DistinctUid['EditDays'] = 2.0  # 唯一值id  91行
    df_DistinctUid['Weekdays'] = 999  # 唯一值id  91行
    df_DistinctUid['Weekends'] = 999  # 唯一值id  91行

    editResult = EditDays()

    p = Pool(5)  # cpu_count 查询当前设备进程数
    for i in range(5):
        begin = i * 2000
        end = (i + 1) * 2000
        p.apply_async(insertSQl, args=[begin, end, editResult])
    p.close()
    p.join()
    endTime0 = datetime.datetime.now()
    print("已完成", endTime0 - startTime)
