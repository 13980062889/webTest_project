'''
============================
@Time    :2020/03/09/13:03
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
class TestAdd(unittest.TestCase):

    excle=ReadExcle(os.path.join(DATA_DIR,"apicases.xlsx"),"add")
    cases=excle.read_data()
    http=SendRequest()
    mysql=HandleMysql()

    @data(*cases)
    def test_add(self,case):
        # 1.请求行 url，method
        add_url=conf.get("env","base_url")+case["url"]
        add_method=case["method"]

        # 2.请求头 headers
        add_headers=eval(conf.get("env","headers_v2"))
        if case["interface"]!="login":
            add_headers["Authorization"]=getattr(TestData,"token_value")

        # 3.请求体 data
        add_data=eval(replace_data(case["data"]))

        # 4.预期结果和回写数据的行数
        add_expected=eval(case["expected"])
        row_num=case["case_id"]+1

        # 5.在发起请求之前，先在数据库查询当前管理员标的数量为start_num
        if case["check_sql"]:
            sql=replace_data(case["check_sql"])
            start_num=self.mysql.get_count(sql)

        # 6.发起请求，获取实际返回结果
        response=self.http.send_requests_v2(url=add_url,method=add_method,headers=add_headers,json=add_data)
        json_data=response.json()

        # 7.登录接口获取返回数据当中的member_id和token
        if case["interface"]=="login":
            # admin_member_id
            admin_member_id=jsonpath.jsonpath(json_data,"$..id")[0]
            setattr(TestData,"admin_member_id",str(admin_member_id))
            # token
            token_type=jsonpath.jsonpath(json_data,"$..token_type")[0]
            token=jsonpath.jsonpath(json_data,"$..token")[0]
            token_value=token_type+" "+token
            setattr(TestData,"token_value",token_value)
        # 8.断言
        try:
            self.assertEqual(add_expected["code"],json_data["code"])
            self.assertEqual(add_expected["msg"],json_data["msg"])
            if case["check_sql"]:
                sql=replace_data(case["check_sql"])
                end_num=self.mysql.get_count(sql)
                self.assertEqual(end_num-start_num,1)
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
        cls.mysql.close()


