'''
============================
@Time    :2020/03/08/14:59
@Author  :cai ming liang
@E-mail  :2117899275@qq.com
============================
'''
import os

# 获取项目的根目录
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 获取配置文件目录的路径
CONF_DIR=os.path.join(BASE_DIR,"config")
# 获取测试数据目录的路径
DATA_DIR=os.path.join(BASE_DIR,"datas")
# 获取日志文件目录的路径
LOG_DIR=os.path.join(BASE_DIR,"logs")
# 获取测试报告目录的路径
REPORT_DIR=os.path.join(BASE_DIR,"reports")
# 获取测试用例目录的路径
CASE_DIR=os.path.join(BASE_DIR,"testcases")