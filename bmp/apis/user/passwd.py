# coding: utf-8
import random

from flask import session

from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION
from bmp.models.user import User
from bmp.utils.exception import ExceptionEx
from bmp.utils.user_ldap import Ldap
from bmp.utils import crypt

class PasswdApi(BaseApi):
    route = ["/users/passwd/<string:uid>", "/users/passwd/<string:uid>/<string:oldpass>",
             "/users/passwd/<string:uid>/<string:oldpass>/<string:newpass>"]

    def put(self, uid, oldpass=None, newpass=None):
        if not oldpass and not User.get(session[USER_SESSION]["uid"])["is_admin"]:
            raise ExceptionEx("权限不足")

        newpass = newpass if newpass else crypt.randpass()

        ldap = Ldap()
        if not ldap.reset_pwd(uid, newpass, oldpass):
            return self.fail()

        return self.succ(newpass)
