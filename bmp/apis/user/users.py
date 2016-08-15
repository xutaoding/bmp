# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.user import User


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
        if not User.update():
            return self.fail()
        return self.succ()
