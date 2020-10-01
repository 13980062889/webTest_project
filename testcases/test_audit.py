'''
============================
@Time    :2020/03/09/13:44
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
from common.handle_replacedata import TestData,replace_data

@ddt
class TestAudit(unittest.TestCase):
    excle=ReadExcle(os.path.join(DATA_DIR,"apicases.xlsx"),"audit")
    cases=excle.read_data()
    http=SendRequest()
    mysql=HandleMysql()

    @data(*cases)
    def test_audit(self,case):
        # 1.请求行 url，method
        audit_url=conf.get("env","base_url")+case["url"]
        audit_method=case["method"]

        # 2.请求头 headers
        audit_headers=eval(conf.get("env","headers_v2"))
        if case["interface"]!="login":
            audit_headers["Authorization"]=getattr(TestData,"token_value")

        # 3.请求体 data
        audit_data=eval(replace_data(case["data"]))

        # 4.预期结果和回写数据的行数
        audit_expected=eval(case["expected"])
        row_num=case["case_id"]+1

        # 5.发起请求，返回数据
        response=self.http.send_requests_v2(url=audit_url,method=audit_method,headers=audit_headers,json=audit_data)
        json_data=response.json()

        # 6.根据接口的类型来判断是否提取token,member_id,loan_id
        if case["interface"]=="login":
            admin_member_id=jsonpath.jsonpath(json_data,"$..id")[0]
            setattr(TestData,"admin_member_id",str(admin_member_id))
            token_type=jsonpath.jsonpath(json_data,"$..token_type")[0]
            token=jsonpath.jsonpath(json_data,"$..token")[0]
            token_value=token_type+" "+token
            setattr(TestData,"token_value",token_value)
        elif case["interface"] == "add":
            loan_id=jsonpath.jsonpath(json_data,"$..id")[0]
            setattr(TestData,"loan_id",str(loan_id))
        elif json_data["msg"]=="OK" and case["title"]=="审核通过":
            pass_loan_id=getattr(TestData,"loan_id")
            setattr(TestData,"pass_loan_id",pass_loan_id)

        # 7.断言
        try:
            self.assertEqual(audit_expected["code"],json_data["code"])
            self.assertEqual(audit_expected["msg"],json_data["msg"])
            if case["check_sql"]:
                sql = replace_data(case["check_sql"])
                status = self.mysql.get_one(sql)["status"]
                self.assertEqual(status,audit_expected["status"])
        except AssertionError as e:
            self.excle.write_data(row=row_num,column=8,value="未通过")
            log.error("用例:{}:未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excle.write_data(row=row_num,column=8,value="通过")
            log.info("用例:{}:通过".format(case["title"]))

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()
