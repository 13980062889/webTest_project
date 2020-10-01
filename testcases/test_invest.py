'''
============================
@Time    :2020/03/09/14:13
@Author  :cai ming liang
@E-mail  :2117899275@qq.com
============================
'''
import os
import unittest
import jsonpath
from library.ddt import ddt,data
from common.handle_log import log
from common.handle_path import DATA_DIR
from common.handle_config import conf
from common.handle_requests import SendRequest
from common.handle_database import HandleMysql
from common.handle_readexcle import ReadExcle
from common.handle_replacedata import replace_data,TestData


@ddt
class TestInvestCase(unittest.TestCase):

    excle=ReadExcle(os.path.join(DATA_DIR,"apicases.xlsx"),"invest")
    cases=excle.read_data()
    http=SendRequest()
    mysql=HandleMysql()

    @data(*cases)
    def test_invest(self,case):
        # 1.请求行，url，method
        invest_url=conf.get("env","base_url")+case["url"]
        invest_method=case["method"]

        # 2.请求头，headers
        invest_headers=eval(conf.get("env","headers_v2"))
        if case["interface"]!="login":
            invest_headers["Authorization"]=getattr(TestData,"token_value")

        # 3.请求体，data
        invest_data=eval(replace_data(case["data"]))

        # 4.预期结果和回写数据的行数
        invest_expected=eval(case["expected"])
        row_num=case["case_id"]+1

        # 5.发起请求之前，现在invest表当中查询当前投资用户对当前标的的投资数量start_num
        if case["check_sql"]:
            query_sql=replace_data(case["check_sql"])
            start_num=self.mysql.get_count(query_sql)

        # 6.发起请求，返回数据
        response=self.http.send_requests_v2(url=invest_url,method=invest_method,headers=invest_headers,json=invest_data)
        json_data=response.json()

        # 7.根据接口的类型来判断是否提取token,member_id,loan_id
        if case["interface"]=="login":
            member_id=jsonpath.jsonpath(json_data,"$..id")[0]
            setattr(TestData,"member_id",str(member_id))
            token_type=jsonpath.jsonpath(json_data,"$..token_type")[0]
            token=jsonpath.jsonpath(json_data,"$..token")[0]
            token_value=token_type+" "+token
            setattr(TestData,"token_value",token_value)
        elif case["interface"]=="add":
            loan_id=jsonpath.jsonpath(json_data,"$..id")[0]
            setattr(TestData,"loan_id",str(loan_id))

        # 8.断言
        try:
            self.assertEqual(invest_expected["code"],json_data["code"])
            self.assertEqual(invest_expected["msg"],json_data["msg"])
            # 发起请求之后，再次在invest表当中查询当前投资用户对当前标的的投资数量end_num
            if json_data["msg"]=="OK" and case["check_sql"]:
                query_sql=replace_data(case["check_sql"])
                end_num=self.mysql.get_count(query_sql)
                self.assertEqual(end_num-start_num,1)
        except AssertionError as e:
            self.excle.write_data(row=row_num,column=8,value="未通过")
            log.error("用例:{}未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excle.write_data(row=row_num,column=8,value="通过")
            log.info("用例:{}通过".format(case["title"]))

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()
