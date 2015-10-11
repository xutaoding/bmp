#coding: utf-8
from bmp.apis.base import BaseApi
from flask import session
from bmp.const import USER_SESSION

class UserApi(BaseApi):
    route="/user"
    def get(self):
        return self.succ(session[USER_SESSION])