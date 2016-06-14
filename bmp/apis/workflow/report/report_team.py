# coding=utf-8

from flask import session

from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION
from bmp.models.report import ReportTeam

class Report_teamApi(BaseApi):
    route = ["/report/team", "/report/team/<int:rid>"]

    def get(self):
        return self.succ(ReportTeam.select())

    def post(self):
        submit = self.request()
        submit["create_uid"] = session[USER_SESSION]["uid"]
        ReportTeam.add(submit)
        return self.succ()

    def delete(self, rid):
        ReportTeam.delete(rid)
        return self.succ()

    def put(self, rid):
        submit = self.request()
        submit["id"] = rid
        ReportTeam.edit(submit)
        return self.succ()


if __name__ == "__main__":
    pass
    # report=Report.add({"schedule":"test","create_time":datetime.now()})
