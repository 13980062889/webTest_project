'''
============================
@Time    :2020/03/08/16:28
@Author  :cai ming liang
@E-mail  :2117899275@qq.com
============================
'''
import os
import unittest
from library.ddt import ddt,data
from common.handle_log import log
from common.handle_path import DATA_DIR
from common.handle_config import conf
from common.handle_requests import SendRequest
from common.handle_readexcle import ReadExcle
from common.handle_replacedata import replace_data

@ddt
class TestLoginCase(unittest.TestCase):

    excle=ReadExcle(os.path.join(DATA_DIR,"apicases.xlsx"),"login")
    cases=excle.read_data()
    http=SendRequest()

    @data(*cases)
    def test_login(self,case):
        # 1.请求行 method url
        login_url=conf.get("env","base_url")+case["url"]
        login_method=case["method"]

        # 2.请求头 headers
        login_headers=eval(conf.get("env","headers_v2"))

        # 3.请求体 data
        case["data"]=replace_data(case["data"])
        login_data=eval(case["data"])

        # 4.预期结果和回写数据的行数
        login_expected=eval(case["expected"])
        row_num = case["case_id"]+1

        # 5.发起请求，获取实际返回结果
        response=self.http.send_requests_v2(url=login_url,method=login_method,headers=login_headers,json=login_data)
        json_data=response.json()

        # 6.断言
        try:
            self.assertEqual(login_expected["code"], json_data["code"])
            self.assertEqual(login_expected["msg"], json_data["msg"])
        except AssertionError as e:
            self.excle.write_data(row=row_num, column=8, value="未通过")
            log.error("用例:{}未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excle.write_data(row=row_num, column=8, value="通过")
            log.info("用例:{}通过".format(case["title"]))
