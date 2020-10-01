'''
============================
@Time    :2020/03/08/16:01
@Author  :cai ming liang
@E-mail  :2117899275@qq.com
============================
'''
import os
from configparser import ConfigParser
from common.handle_path import CONF_DIR


class HandleConfig(ConfigParser):

    def __init__(self,config_file):
        self.config_file=config_file
        super().__init__()
        self.read(config_file,encoding="utf8")

    def write_data(self,section,option,value):
        self.set(section,option,value)
        self.write(fp=open(self.config_file,"w"))

conf=HandleConfig(os.path.join(CONF_DIR,"config.ini"))
