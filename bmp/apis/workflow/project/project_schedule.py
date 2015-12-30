# coding: utf-8
from flask import session

from bmp.apis.base import BaseApi
from bmp.models.project import ProjectSchedule
from bmp.const import USER_SESSION


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
    pass
