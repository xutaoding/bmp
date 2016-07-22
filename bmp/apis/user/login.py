# coding: utf-8
from flask import session

from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION, KEY_SESSION
from bmp.models.user import User
from bmp.utils import crypt
from bmp.utils.exception import ExceptionEx
from bmp.utils.user_ldap import Ldap


class LoginApi(BaseApi):
    route = "/login/<string:uid>/<string:pwd>"

    def auth(self):
        return True

    def get(self, uid, pwd):

        if session.__contains__(USER_SESSION):
            User.add(session[USER_SESSION])
            return self.fail("已登录")

        if not session.__contains__(KEY_SESSION):
            raise ExceptionEx("未申请密钥")

        uid = crypt.desc(uid)
        pwd = crypt.desc(pwd)

        ldap = Ldap()
        if not ldap.auth(uid, pwd):
            return self.fail("用户名或密码错误")

        dn, _user = ldap.search(uid).first()

        User.add(_user)
        session[USER_SESSION] = _user
        return self.succ(session[USER_SESSION])
