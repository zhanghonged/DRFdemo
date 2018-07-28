#!/usr/bin/python
# coding:utf-8

import requests


class GetToken:
    def __init__(self,url,data):
        self.url =url
        self.data = data

    def getres(self):
        self.response = requests.post(url=self.url,data=self.data)
        return self.response.json()['token']

if __name__ == "__main__":
    loginurl = "http://192.168.1.222:8000/login/"

    loginData = {
        "username": "daimeng@16feng.com",
        "password": "123456"
    }
    a = GetToken(loginurl,loginData)
    print(a.getres())