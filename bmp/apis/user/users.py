# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.user import User
import bmp.utils.user_ldap as ldap


class UsersApi(BaseApi):
    route = ["/users", "/users/<string:uid>"]

    def get(self, uid="%"):
        return self.succ(User.select(uid))

    def put(self):
        submit = self.request()
        User.edit(submit)
        return self.succ()

    def delete(self, uid):
        User.delete(uid)
        return self.succ()

    def groups(self, uid):
        submit = self.request()
        User.set_groups(uid, submit["groups"])
        return self.succ()

    def update(self):
        if not User.update(ldap.all()):
            return self.fail()
        return self.succ()


if __name__ == "__main__":
    import requests
    requests.post("http://192.168.0.227",data={"data":"5"}.__str__())
