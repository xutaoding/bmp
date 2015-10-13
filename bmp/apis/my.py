#coding: utf-8
from bmp.apis.base import BaseApi
from flask import session
from bmp.const import USER_SESSION

class MyApi(BaseApi):
    route="/my"
    def get(self):
        return self.succ(session[USER_SESSION])


    def put(self):
        pass


    def post(self):
        pass