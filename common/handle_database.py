'''
============================
@Time    :2020/03/08/16:01
@Author  :cai ming liang
@E-mail  :2117899275@qq.com
============================
'''
import pymysql
from common.handle_config import conf

class HandleMysql():

    def __init__(self):
        # 连接到数据库
        self.connect=pymysql.connect(host=conf.get("mysql","host"),
                                     port=conf.getint("mysql","port"),
                                     user=conf.get("mysql","username"),
                                     password=conf.get("mysql", "password"),
                                     charset=conf.get("mysql", "charset"),
                                     cursorclass=pymysql.cursors.DictCursor
                                     )
        # 创建一个游标对象
        self.cursor=self.connect.cursor()

    def get_one(self,sql):
        '''获取查询到的第一条数据'''
        self.connect.commit()
        self.cursor.execute(sql)
        return self.cursor.fetchone()  # 默认返回的是一个字典，如果要变类型，可以通过指定游标类型

    def get_all(self, sql):
        '''获取查询到的所有数据'''
        self.connect.commit()
        self.cursor.execute(sql)
        return self.cursor.fetchall()  # 返回的是一个字典，如果要变类型，可以通过指定游标类型

    def get_count(self, sql):
        '''获取查询到的数据数量'''
        self.connect.commit()
        res=self.cursor.execute(sql)
        return res  # 返回的是数字

    def close(self):
        '''关闭游标，断开连接'''
        self.cursor.close()
        self.connect.close()
