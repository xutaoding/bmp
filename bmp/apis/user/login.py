# coding: utf-8
import rsa
from flask import session

from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION, KEY_SESSION
from bmp.models.user import User
from bmp.utils import user_ldap
from bmp.utils.exception import ExceptionEx


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

        pkey = session[KEY_SESSION]
        prikey = rsa.PrivateKey(pkey["n"], pkey["e"], pkey["d"], pkey["p"], pkey["q"])
        uid,pwd = rsa.decrypt(uid,prikey),rsa.decrypt(pwd,prikey)

        result, _user = user_ldap.auth(uid,pwd)
        if not result:
            return self.fail("用户名或密码错误")

        
        User.add(_user)
        session[USER_SESSION] = _user
        return self.succ(session[USER_SESSION])
