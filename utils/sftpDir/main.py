#!/usr/bin/python
# coding:utf-8

from getJwt import GetToken
from getData import GetData
from sendData import Sender
import sys

import requests,json


# url地址
url = 'http://192.168.1.222:8000/servers/' + sys.argv[1] + '/'
loginurl = "http://192.168.1.222:8000/login/"

loginData = {
"username":"daimeng@16feng.com",
"password":"123.com"
}

# 请求登录接口获取token
getlogin = GetToken(loginurl,loginData)
token = getlogin.getres()
headers = {
  'content-type': 'application/json',
  "Authorization":"JWT "+token}

#采集数据
mydata = GetData()
sendData = mydata.getData()
# 发送数据
sender = Sender(url,sendData,headers)
sender.get_request()
response = sender.get_response()

# 获取响应
print(response)
