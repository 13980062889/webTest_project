'''
============================
@Time    :2020/03/01/14:13
@Author  :cai ming liang
@E-mail  :2117899275@qq.com
============================
'''
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from common.handle_path import REPORT_DIR

def send_email():

    # 1.连接到SMTP服务器
    smtp=smtplib.SMTP_SSL("smtp.qq.com",465)
    smtp.login("2117899275@qq.com","mmraqtljcvmzcfgi")

    # 2.构建一封邮件
    msg=MIMEMultipart()
    msg_text=MIMEText(open(os.path.join(REPORT_DIR,"requests_report.html"),"rb").read(),"html","utf8")
    msg.attach(msg_text)

    msg_file=MIMEApplication(open(os.path.join(REPORT_DIR,"requests_report.html"),"rb").read())
    msg_file.add_header("content-disposition","attachment",filename='report.html')
    msg.attach(msg_file)

    msg["Subject"]="测试报告"
    msg["From"]="2117899275@qq.com"
    msg["To"]="migliangcai@163.com"
    msg["Cc"]="324287622@qq.com"

    # 3.发送邮件
    smtp.send_message(msg,from_addr="2117899275@qq.com",to_addrs="mingliangcai@163.com")
