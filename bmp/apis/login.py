#coding: utf-8
from flask import session

from bmp.apis.base import BaseView
from bmp.models import user_ldap
from bmp.const import USER_SESSION

sample={
    "result":True,#true,false
    "error":"",#
    "content":{}
}

class LoginView(BaseView):
    def auth(self):
        return True

    def get(self,name,pwd):
        if session.__contains__(USER_SESSION):
            return self.success(session[USER_SESSION])
        result,user=user_ldap.auth(name,pwd)

        if result:
            session[USER_SESSION]=user.to_dict()
            return self.success(session[USER_SESSION])

        return self.failure("用户名或密码错误")