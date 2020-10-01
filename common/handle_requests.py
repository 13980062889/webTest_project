'''
============================
@Time    :2020/03/01/14:03
@Author  :cai ming liang
@E-mail  :2117899275@qq.com
============================
'''
import requests

class SendRequest(object):

    def __init__(self):
        self.session=requests.session()

    def send_requests_v2(self,url,method,params=None,json=None,data=None,files=None,headers=None):
        method=method.lower()
        if method=="get":
            response=self.session.get(url=url,params=params,headers=headers)
        elif method=="post":
            response=self.session.post(url=url,json=json,data=data,files=files,headers=headers)
        elif method=="patch":
            response=self.session.patch(url=url,json=json,data=data,files=files,headers=headers)

        return response
