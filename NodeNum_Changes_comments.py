import datetime
import pandas as pd
import sqlalchemy
from multiprocessing import cpu_count, Pool
import pymysql
import gc
from tqdm import tqdm

db = pymysql.Connect(
    host='localhost',
    user='root',
    password='zxcvbnm,./',
    database='osm',
    port=3306,
    charset='utf8',
    autocommit=True
)
def editNode():
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
    print("-------------数据处理中---------------")
    for idrow in tqdm(range(0,len(df_DistinctUid))):
        df_DistinctUid.iloc[idrow,1] = allNum[str(df_DistinctUid.iloc[idrow,0])]
        df_DistinctUid.iloc[idrow,2] = allSum.loc[str(df_DistinctUid.iloc[idrow,0]),'num_changes']
        df_DistinctUid.iloc[idrow,3] = allSum.loc[str(df_DistinctUid.iloc[idrow,0]),'comments_count']
    print("-------------数据处理已完成，准备数据导入---------------")
    # df_DistinctUid.to_excel("D:/Desktop/data/ NodeNum_Changes_comments.xlsx")
    return df_DistinctUid

def insertSQl(begin, end, editResult):
    insersql = 'INSERT INTO volunteer(NodeNum,NumChanges,Comments_Count) VALUES'
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
            insersql = 'INSERT INTO volunteer(NodeNum,NumChanges,Comments_Count) VALUES'
        insersql += f"('{editResult.iloc[i, 1]}','{editResult.iloc[i, 2]}','{editResult.iloc[i, 3]}'),"
        print(insersql)

if __name__ == '__main__':
    startTime = datetime.datetime.now()
    print("-------------读取数据中---------------")
    engine = sqlalchemy.create_engine('mysql+pymysql://root:zxcvbnm,./@localhost:3306/osm')
    sql_DistinctUid = f'''
    select distinct uid from test10000 order by (uid+0) asc
    '''
    df_DistinctUid = pd.read_sql(sql_DistinctUid, engine)

    df_DistinctUid['NodeNum'] = 999
    df_DistinctUid['NumChanges'] = 999999
    df_DistinctUid['Comments_Count'] = 999999

    editResult = editNode()

    p = Pool(5)  # cpu_count 查询当前设备进程数
    for i in range(5):
        begin = i * 2000
        end = (i + 1) * 2000
        p.apply_async(insertSQl, args=[begin, end, editResult])
    p.close()
    p.join()
    endTime0 = datetime.datetime.now()
    print("已完成", endTime0 - startTime)