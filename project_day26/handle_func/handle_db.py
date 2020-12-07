
import pymysql
from handle_func.handle_config import conf
import random
class DB:
    def __init__(self,host,port,user,password):
        # 第一步：连接数据库
        self.con=pymysql.connect(host=host,
                    port=port,
                    user=user,
                    password=password,
                    charset="utf8",
                    cursorclass=pymysql.cursors.DictCursor
                    )
         # 第二步：创建一个游标
        self.cur=self.con.cursor()
    def find_data(self,sql):
        self.con.commit()
        self.cur.execute(sql)
        res=self.cur.fetchall()
        # print(res)
        return res
db=DB(host=conf.get("database","host"),
      port=int(conf.get("database","port")),
      user=conf.get("database","user"),
      password=conf.get("database","password")

)

if __name__=="__main__":
    sql = "select mobile_phone from futureloan.member where mobile_phone=15898634757"
    res = db.find_data(sql)
