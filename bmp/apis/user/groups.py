# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.user import Group

class GroupsApi(BaseApi):
    route=["/groups","/groups/<string:name>","/groups/<string:name>/<string:new>"]
    def get(self,name="%"):
        return self.succ([g.to_dict() for g in Group.query.filter(Group.name.like(name)).all()])

    def put(self,name,new=""):
        if new:
            if not Group.edit(name,new):
                return self.fail()
            return self.succ()

        submit=self.request()
        if not Group.join(name,submit.split(",")):
            return self.fail()
        return self.succ()

    def post(self,name):
        if not Group.add(name):
            return self.fail()
        return self.succ()

    def delete(self,name):
        Group.delete(name)
        return self.succ()
