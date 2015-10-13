#coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.user import Group,add_group,join_group,edit_group,delete_group

class GroupsApi(BaseApi):
    route=["/groups","/groups/<string:name>","/groups/<string:name>/<string:new>"]
    def get(self,name="%"):
        return self.succ([g.to_dict() for g in Group.query.filter(Group.name.like(name)).all()])

    def put(self,name,new=""):
        if new:
            if not edit_group(name,new):
                return self.fail()
            return self.succ()

        submit=self.request()
        if not join_group(name,submit):
            return self.fail()
        return self.succ()

    def post(self,name):
        if not add_group(name):
            return self.fail()
        return self.succ()

    def delete(self,name):
        delete_group(name)
        return self.succ()
