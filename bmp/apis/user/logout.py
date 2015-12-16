# coding: utf-8
from flask import session

from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION


class LogoutApi(BaseApi):
    route = "/logout"

    def get(self):
        session.pop(USER_SESSION)
        return self.succ()
