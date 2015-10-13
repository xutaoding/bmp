#coding: utf-8
from flask import session
from bmp.apis.base import BaseApi
from bmp.utils import user_ldap
from bmp.const import USER_SESSION
import bmp.models.user as user

class LoginApi(BaseApi):
    route="/login/<string:uid>/<string:pwd>"
    def auth(self):
        return True

    def get(self,uid,pwd):
        if session.__contains__(USER_SESSION):
            return self.fail("已登录")

        result,_user= user_ldap.auth(uid,pwd)
        if result:
            user.add(_user)
            session[USER_SESSION]=_user
            return self.succ(session[USER_SESSION])

        return self.fail("用户名或密码错误")