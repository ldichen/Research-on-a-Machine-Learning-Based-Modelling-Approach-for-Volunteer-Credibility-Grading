import pandas as pd
import sqlalchemy
import pymysql

db_conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="zxcvbnm,./",
    database="osm",
    charset="utf8"
)

# engine = sqlalchemy.create_engine('mysql+pymysql://root:zxcvbnm,./@localhost:3306/osm')
sql = "select distinct uid from a1_9999999 order by (uid+0) asc"

df = pd.read_sql(sql, db_conn)  # uid解决
# print(df)
df.to_excel("D:/Desktop/data/uid.xlsx")
