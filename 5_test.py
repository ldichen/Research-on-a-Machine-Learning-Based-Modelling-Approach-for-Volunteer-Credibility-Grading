from multiprocessing import cpu_count, Pool

def be(begin,end):
    print(begin,end)
    print(df_DistinctUid)

if __name__ == '__main__':
    df_DistinctUid = 2.0  # 唯一值id  91行
    p = Pool(5)  # cpu_count 查询当前设备进程数
    for i in range(5):
        begin = i * 2000
        end = (i + 1) * 2000
        p.apply_async(be, args=[begin, end])
    p.close()
    p.join()