# coding: utf-8
from flask import session

from bmp.apis.base import BaseApi
from bmp.models.project import ProjectSchedule
from bmp.const import USER_SESSION


class Project_memberApi(BaseApi):
    route = ["/project/member/<int:sid>"]

    def put(self, sid):
        submit = self.request()
        submit["schedule_id"] = sid
        ProjectSchedule.edit_members(submit)
        return self.succ()


if __name__ == "__main__":
    pass