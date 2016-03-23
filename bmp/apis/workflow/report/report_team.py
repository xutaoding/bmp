# coding=utf-8
from datetime import datetime

from bmp.apis.base import BaseApi
from bmp.models.report import Report,ReportTeam
from datetime import datetime
from datetime import timedelta


class Report_teamApi(BaseApi):
    route = ["/report/team","/report/team/<int:rid>"]

    def get(self):
        return self.succ(ReportTeam.select())

    def post(self):
        submit=self.request()
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
