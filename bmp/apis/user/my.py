# coding: utf-8
from flask import session

from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION
from bmp.models.user import User
from bmp.utils import user_ldap


class MyApi(BaseApi):
    route = ["/my"]

    def get(self):
        return self.succ(User.get(session[USER_SESSION]["uid"]))

    def put(self):
        submit = self.request()
        if submit.__contains__("mobile"):
            user_ldap.modify(session[USER_SESSION]["uid"],
                             submit["password"],
                             {"mobile": submit["mobile"]},
                             {"mobile": submit["mobile"]})
        User.edit(submit)
        return self.succ()

    def post(self):
        pass
