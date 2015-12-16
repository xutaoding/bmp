# coding: utf-8
from bmp import db
from bmp.apis.base import BaseApi
from bmp.models.project import ProjectSchedule
from flask import session
from bmp.const import USER_SESSION

class Project_memberApi(BaseApi):
    route = ["/project/member/<int:sid>"]
    def auth(self):
        session[USER_SESSION]={"uid":"chenglong.yan"}
        return True

    def put(self,sid):
        submit=self.request()
        submit["schedule_id"]=sid
        ProjectSchedule.edit_members(submit)
        return self.succ()



if __name__ == "__main__":
    from bmp.utils.post import test
    test("put",
         "http://127.0.0.1:5000/apis/v1.0/project/member/1",
         {
             "members":[
                        {"uid":"chenglong.yan"},
                        {"uid":"mingming.zhang"}
                    ]
         },True)