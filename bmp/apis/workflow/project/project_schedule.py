# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.project import ProjectSchedule
from flask import session
from bmp.const import USER_SESSION

class Project_scheduleApi(BaseApi):
    route = ["/project/schedule/<int:pid>"]
    def auth(self):
        session[USER_SESSION]["uid"]="chenglong.yan"
        return True

    def post(self,pid):
        submit=self.request()
        submit["project_id"]=pid
        ProjectSchedule.add(submit)
        return self.succ()

    def put(self,pid):
        submit=self.request()
        submit["project_id"]=pid
        ProjectSchedule.edit(submit)
        return self.succ()


if __name__ == "__main__":
    from bmp.utils.post import test
    test("post",
         "127.0.0.1:5000/apis/v1.0/project",
         {
             "type":"demand",#需求阶段
             "begin_time":"1990-01-01",#需求周期
             "end_time":"1990-01-02",#需求周期
             "status":"1",#refs的id,项目状态
             "reson":"",
             "desc":""
         },True)