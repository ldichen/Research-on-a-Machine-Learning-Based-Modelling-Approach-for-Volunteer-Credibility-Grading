import datetime

if __name__ == '__main__':
    ft = "2006-11-30T10:07:01Z"
    lt = "2009-04-16T13:30:35Z"

    f = "2006-11-30T10:07:01Z"
    l = "2006-11-30T13:30:35Z"

    t1 = datetime.datetime.strptime(f, "%Y-%m-%dT%H:%M:%SZ")
    t2 =  datetime.datetime.strptime(l, "%Y-%m-%dT%H:%M:%SZ")


    test = (datetime.datetime.strptime(lt, "%Y-%m-%dT%H:%M:%SZ") - datetime.datetime.strptime(ft, "%Y-%m-%dT%H:%M:%SZ"))

    print(t1.date())
    print(t2.date())
    print((t1.date() == t2.date()))
    print(test)
