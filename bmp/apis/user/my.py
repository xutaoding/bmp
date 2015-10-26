#coding: utf-8
from bmp.apis.base import BaseApi
from flask import session
from bmp.const import USER_SESSION
from bmp.models.user import User

class MyApi(BaseApi):
    route=["/my"]
    def get(self):
        return self.succ(User.get(session[USER_SESSION]["uid"]))

    def put(self):
        pass

    def post(self):
        pass