'''
============================
@Time    :2020/03/09/14:44
@Author  :cai ming liang
@E-mail  :2117899275@qq.com
============================
'''
import unittest
import os
from common.handle_path import CASE_DIR,REPORT_DIR
from library.HTMLTestRunnerNew import HTMLTestRunner


# 第一步：创建套件
suite = unittest.TestSuite()

# 第二步：加载用例到套件，有4种方式
    # 1.通过模块去加载用例
# suite.addTest(loader.loadTestsFromModule(testcase))
    # 2.通过测试用例类去加载用例
# suite.addTest(loader.loadTestsTestCase(testcase.LoginTest))
    # 3.添加单条测试用例
# suite.addTest(LoginTest("test_login"))

loader = unittest.TestLoader()
suite.addTest(loader.discover(CASE_DIR))

report_file = os.path.join(REPORT_DIR,"apireport.html")

# 第三步：执行用例
runner = HTMLTestRunner(stream=open(report_file, "wb"),
                        description="api接口测试报告",
                        title="api测试报告",
                        tester="cbz"
                        )
runner.run(suite)