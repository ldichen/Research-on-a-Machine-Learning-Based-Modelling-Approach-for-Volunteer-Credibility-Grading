"""多进程"""
import datetime
import gc
from multiprocessing import cpu_count, Pool
import pymysql
from tqdm import tqdm

db = pymysql.Connect(
    host='localhost',
    user='root',
    password='zxcvbnm,./',
    database='test',
    port=3306,
    charset='utf8',
    autocommit=True
)


def insertSQl(begin, end):
    print(datetime.datetime.now())
    sql = 'INSERT INTO pool2(id,name) VALUES'

    for i in tqdm(range(begin, end)):  # python进度条 tqdm
        if i % 10000 == 0:  # 每10000次进行一次插入，速度没有经过校验，不确定10000万次是否为最佳
            sql = sql.strip(',\n')  # sql语句拼接时最后会留下一个逗号，不删除会报错
            try:
                db.ping(reconnect=True)  # reconnect 自动重联
                cur = db.cursor()
                cur.execute(sql)
                db.commit()
                cur.close()
                db.close()
                del sql  # 删除变量
                gc.collect()  # 回收内存空间

            except Exception as e:
                print(e)
            # sql重置
            sql = 'INSERT INTO pool2(id,name) VALUES'
        sql += f"('{i}','name_{i}'),"


if __name__ == '__main__':
    startTime = datetime.datetime.now()
    print(startTime)
    p = Pool(2)  # cpu_count 查询当前设备进程数，我的是八核，所以下面分了8个进程
    p.apply_async(insertSQl, args=[1, 1250001])
    p.apply_async(insertSQl, args=[1250001, 2500001])
    # p.apply_async(insertSQl, args=[2500001, 3750001])
    # p.apply_async(insertSQl, args=[3750001, 5000001])
    # p.apply_async(insertSQl, args=[5000001, 6250001])
    # p.apply_async(insertSQl, args=[6250001, 7500001])
    # p.apply_async(insertSQl, args=[7500001, 8750001])
    # p.apply_async(insertSQl, args=[8750001, 10000001])

    p.close()
    p.join()
    endTime = datetime.datetime.now()
    print(endTime - startTime)
