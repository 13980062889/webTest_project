'''
============================
@Time    :2020/03/09/10:37
@Author  :cai ming liang
@E-mail  :2117899275@qq.com
============================
'''
import os
import unittest
import jsonpath
from decimal import Decimal
from library.ddt import ddt,data
from common.handle_log import log
from common.handle_path import DATA_DIR
from common.handle_config import conf
from common.handle_requests import SendRequest
from common.handle_database import HandleMysql
from common.handle_readexcle import ReadExcle
from common.handle_replacedata import replace_data,TestData


@ddt
class TestRechargeCase(unittest.TestCase):

    excle=ReadExcle(os.path.join(DATA_DIR,"apicases.xlsx"),"recharge")
    cases=excle.read_data()
    http=SendRequest()
    mysql=HandleMysql()

    @data(*cases)
    def test_recharge(self,case):
        # 1.请求行 method url
        recharge_url=conf.get("env","base_url")+case["url"]
        recharge_method=case["method"]

        # 2.请求头 headers
        recharge_headers=eval(conf.get("env","headers_v2"))
        if case["interface"]!="login":
            recharge_headers["Authorization"]=getattr(TestData,"token_value")

        # 3.请求体 data
        recharge_data=eval(replace_data(case["data"]))

        # 4.预期结果和回写数据的行数
        recharge_expected=eval(case["expected"])
        row_num=case["case_id"]+1

        # 5.充值前先检查数据库当中的余额start_money
        if case["check_sql"]:
            sql="SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}".format(conf.get("test_data", "username"))
            start_money=self.mysql.get_one(sql)["leave_amount"]

        # 6.发起请求，获取实际返回结果
        response = self.http.send_requests_v2(url=recharge_url,method=recharge_method,headers=recharge_headers,json=recharge_data)
        infact_result = response.json()

        # 7.充值后再检查数据库当中的余额end_money
        if case["check_sql"]:
            sql = "SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}".format(conf.get("test_data", "username"))
            end_money = self.mysql.get_one(sql)["leave_amount"]

        # 8.登录接口要获取返回数据当中的member_id和token
        if case["interface"]=="login":
            # member_id
            member_id=jsonpath.jsonpath(infact_result,"$..id")[0]
            setattr(TestData,"member_id",str(member_id))
            # token
            token_type=jsonpath.jsonpath(infact_result,"$..token_type")[0]
            token=jsonpath.jsonpath(infact_result,"$..token")[0]
            token_value=token_type+ " " +token
            setattr(TestData,"token_value",token_value)

        # 9.断言
        try:
            self.assertEqual(recharge_expected["code"], infact_result["code"])
            self.assertEqual(recharge_expected["msg"], infact_result["msg"])
            if case["check_sql"]:
                self.assertEqual(end_money - start_money, Decimal(str(recharge_data["amount"])))
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




