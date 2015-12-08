# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.user import Group


class GroupsApi(BaseApi):
    route = ["/groups",
             "/groups/<string:name>/<string:desc>",
             "/groups/<string:name>",
             "/groups/<string:name>/<string:new>/<string:desc>"]

    def get(self, name="%"):
        return self.succ(Group.select(name))

    def put(self, name, new="",desc=""):
        if new:
            if not Group.edit(name,new,desc):
                return self.fail()
            return self.succ()

        submit = self.request()
        if not Group.join(name, submit.split(",")):
            return self.fail()
        return self.succ()

    def post(self, name,desc):
        if not Group.add(name,desc):
            return self.fail()
        return self.succ()

    def delete(self, name):
        Group.delete(name)
        return self.succ()
