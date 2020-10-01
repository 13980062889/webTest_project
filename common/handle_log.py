'''
============================
@Time    :2020/03/08/16:02
@Author  :cai ming liang
@E-mail  :2117899275@qq.com
============================
'''
import os
import logging
from common.handle_config import conf
from common.handle_path import LOG_DIR

class UseLog():

    @staticmethod
    def creat_log():
        '''封装日志收集器'''
        # 1.创建日志收集器，设置收集器等级
        log_collector=logging.getLogger("caibaozi")
        log_collector.setLevel(conf.get("log","collect_level"))

        # 2.创建输出到控制台的渠道，设置输出等级
        sh=logging.StreamHandler()
        sh.setLevel(conf.get("log","sh_level"))
        log_collector.addHandler(sh)

        # 3.创建输出到日志文件的渠道，设置输出等级
        fh=logging.FileHandler(filename=os.path.join(LOG_DIR,"mylog.log"),mode="a",encoding="utf8")
        fh.setLevel(conf.get("log","fh_level"))
        log_collector.addHandler(fh)

        # 4.设置日志输出格式
        format_str = '%(asctime)s-[%(filename)s-->line:%(lineno)d]-%(levelname)s:%(message)s'
        fm=logging.Formatter(format_str)

        # 5.绑定输出格式到控制台，文件
        sh.setFormatter(fm)
        fh.setFormatter(fm)

        return log_collector

log=UseLog.creat_log()