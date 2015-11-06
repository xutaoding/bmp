#coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.user import User
import bmp.utils.user_ldap as ldap

class UsersApi(BaseApi):
    route=["/users","/users/<string:uid>","/users/<string:uid>/<string:email>/<int:is_admin>"]
    def auth(self):
        return True
    def get(self,uid="%"):
        return self.succ(User.select(uid))

    def put(self,uid,email,is_admin):
        User.edit(uid,email,is_admin)
        return self.succ()

    def delete(self,uid):
        User.delete(uid)
        return self.succ()

    def update(self):
        if not User.update(ldap.all()):
            return self.fail()
        return self.succ()



if __name__=="__main__":
    from bmp.utils.post import test
    test("update","http://localhost:5000/apis/v1.0/users",{"test":"test"},True)