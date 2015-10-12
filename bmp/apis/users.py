#coding: utf-8
from bmp.apis.base import BaseApi
from flask import session
from bmp.const import USER_SESSION
from bmp.utils import user_ldap

class UsersApi(BaseApi):
    route="/users/<string:uid>"
    def get(self,uid):
        result=user_ldap.search(uid)
        users=[]
        for dn,user in result:
            users.append(user)
        return self.succ(users)