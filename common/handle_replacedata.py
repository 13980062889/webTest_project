'''
============================
@Time    :2020/03/01/14:34
@Author  :cai ming liang
@E-mail  :2117899275@qq.com
============================
'''
import re
from common.handle_config import conf

class TestData():
    '''这个类的作用是用于存储在执行用例的时候一些要临时替换的数据'''
    pass

def replace_data(data):
    rule=r"#(.+?)#"
    while re.search(rule,data):
        result=re.search(rule,data)
        item=result.group()
        key=result.group(1)
        try:
            data=data.replace(item,conf.get("test_data",key))
        except:
            data = data.replace(item,getattr(TestData,key))
    return data
