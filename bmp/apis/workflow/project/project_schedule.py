# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.project import ProjectSchedule


class Project_scheduleApi(BaseApi):
    route = ["/project/schedule/<int:pid>"]

    def post(self, pid):
        submit = self.request()
        submit["project_id"] = pid
        ProjectSchedule.add(submit)
        return self.succ()

    def put(self, pid):
        submit = self.request()
        submit["project_id"] = pid
        ProjectSchedule.edit(submit)
        return self.succ()


if __name__ == "__main__":





    def sched(id,time):
        return {
            "type":"release",
            "begin_time":time,
            "end_time":time,
            "status":"完成",
            "project_id":id
        }

    ProjectSchedule.add(sched(6,"2016-01-13"))
    ProjectSchedule.add(sched(7,"2016-01-08"))
    ProjectSchedule.add(sched(8,"2016-01-20"))
    ProjectSchedule.add(sched(9,"2016-02-01"))
    ProjectSchedule.add(sched(10,"2016-01-26"))
