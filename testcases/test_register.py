'''
============================
@Time    :2020/03/08/16:28
@Author  :cai ming liang
@E-mail  :2117899275@qq.com
============================
'''
import os
import random
import unittest
from library.ddt import ddt,data
from common.handle_log import log
from common.handle_path import DATA_DIR
from common.handle_config import conf
from common.handle_database import HandleMysql
from common.handle_requests import SendRequest
from common.handle_readexcle import ReadExcle
from common.handle_replacedata import replace_data,TestData


@ddt
class TestRegisterCase(unittest.TestCase):

    excle=ReadExcle(os.path.join(DATA_DIR,"apicases.xlsx"),"register")
    cases=excle.read_data()
    http=SendRequest()
    mysql=HandleMysql()

    def generate_phone(self):
        '''生成随机的手机号码'''
        phone="135"
        num=random.randint(100000000, 999999999)
        phone += str(num)[1:]
        # 随机生成的手机号码后，先查询下数据库当中是否这个手机号码，要是存在就不用
        query_sql="SELECT * FROM futureloan.member WHERE mobile_phone={}".format(phone)
        query_result=self.mysql.get_count(query_sql)
        if query_result==0:
            return phone
        else:
            log.info("该随机生成的手机号码{}已经存在！".format(phone))


    @data(*cases)
    def test_register(self,case):
        # 1.请求行 method url
        register_url=conf.get("env","base_url")+case["url"]
        register_method=case["method"]

        # 2.请求体 data
        if "#phone#" in case["data"]:
            phone=self.generate_phone()
            setattr(TestData,"phone",phone)
            case["data"]=replace_data(case["data"])
        register_data=eval(case["data"])

        # 3.请求头 headers
        register_headers=eval(conf.get("env", "headers_v2"))

        # 4.预期结果和回写数据的行数
        register_expected=eval(case["expected"])
        row_num=case["case_id"]+1
        # 5.发起请求，获取实际返回结果
        response = self.http.send_requests_v2(url=register_url,method=register_method,headers=register_headers,json=register_data)
        infact_result = response.json()

        # 6.断言
        try:
            self.assertEqual(register_expected["code"], infact_result["code"])
            self.assertEqual(register_expected["msg"], infact_result["msg"])
            if register_expected["msg"]=="OK" and case["check_sql"]:
                register_sql=replace_data(case["check_sql"])
                count = self.mysql.get_count(register_sql)
                self.assertEqual(1,count)
        except AssertionError as e:
            self.excle.write_data(row=row_num, column=8, value="未通过")
            log.error("用例:{}未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excle.write_data(row=row_num, column=8, value="通过")
            log.info("用例:{}通过".format(case["title"]))

    @classmethod
    def tearDownClass(cls):
        '''最后关闭数据库的游标和连接'''
        cls.mysql.close()


