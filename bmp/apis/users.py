#coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.user import User,edit,delete

class UsersApi(BaseApi):
    route=["/users","/users/<string:uid>","/users/<string:uid>/<string:email>/<int:is_admin>"]
    def get(self,uid="%"):
        return self.succ([u.to_dict() for u in User.query.filter(User.uid.like(uid)).all()])

    def put(self,uid,email,is_admin):
        edit(uid,email,is_admin)
        return self.succ()

    def delete(self,uid):
        delete(uid)
        return self.succ()