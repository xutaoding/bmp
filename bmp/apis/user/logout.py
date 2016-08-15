# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION
from flask import session


class LogoutApi(BaseApi):
    route = "/logout"

    def get(self):
        session.pop(USER_SESSION)
        return self.succ()
