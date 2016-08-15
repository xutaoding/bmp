# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION
from bmp.models.user import User
from bmp.utils import crypt
from bmp.utils.exception import ExceptionEx
from bmp.utils.user_ldap import Ldap
from flask import session


class PasswdApi(BaseApi):
    route = ["/users/passwd/<string:uid>",
             "/users/passwd/<string:uid>/<string:oldpass>",
             "/users/passwd/<string:uid>/<string:oldpass>/<string:newpass>"]

    def auth(self):
        return True

    def put(self, uid, oldpass=None, newpass=None):
        if not oldpass:
            if not session.__contains__(USER_SESSION):
                raise ExceptionEx("未登录")

            if not User.get(session[USER_SESSION]["uid"])["is_admin"]:
                raise ExceptionEx("权限不足")

        if not uid or uid in ["*", u"*"]:
            return self.fail("无效的用户名")

        newpass = newpass if newpass else crypt.randpass()

        ldap = Ldap()
        if not ldap.reset_pwd(uid, newpass, oldpass):
            return self.fail()

        return self.succ({"new_password": newpass})
