#!/usr/bin/python
# coding:utf-8

import requests, json


class Sender:
    def __init__(self,url,data,headers):
        self.url = url
        self.headers = headers
        self.data = json.dumps(data)
    def get_request(self):
        self.response =requests.patch(self.url,data=self.data,headers=self.headers)
    def get_response(self):
        result = self.response.content
        return result
