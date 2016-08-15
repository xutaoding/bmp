# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION
from bmp.models.user import User
from bmp.utils.user_ldap import Ldap
from flask import session


class MyApi(BaseApi):
    route = ["/my"]

    def get(self):
        return self.succ(User.get(session[USER_SESSION]["uid"]))

    def put(self):
        submit = self.request()
        if submit.__contains__("mobile"):
            ldap = Ldap()
            ldap.modify(session[USER_SESSION]["uid"], {"mobile": submit["mobile"]}, submit["password"])
        User.edit(submit)
        return self.succ()

    def post(self):
        pass
