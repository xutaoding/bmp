# coding=utf-8
from datetime import datetime

from bmp.apis.base import BaseApi
from bmp.models.report import Report
from datetime import datetime
from datetime import timedelta


class ReportApi(BaseApi):
    route = [
        "/report",
        "/report/<int:year>/<int:weeks>",
        "/report/<int:year>/<int:weeks>/<int:team_id>",
        "/report/<int:rid>"
    ]

    def get(self, year, weeks, team_id=None):
        dt = datetime(year, 1, 1) + timedelta(weeks=weeks-1)
        beg_time = dt - timedelta(days=dt.weekday())
        end_time = (dt + timedelta(days=6 - dt.weekday())).replace(hour=23, minute=59, second=59)
        if team_id:
            result=Report.select(
                _filters=[Report.create_time.between(beg_time, end_time), Report.team_id == team_id])
        else:
            result=Report.select(
                _filters=[Report.create_time.between(beg_time, end_time)])

        return self.succ(result)


    def post(self):
        submit = self.request()
        submit["create_time"] = datetime.now()
        Report.add(submit)
        return self.succ()

    def delete(self, rid):
        Report.delete(rid)
        return self.succ()

    def put(self, rid):
        submit = self.request()
        submit["id"] = rid
        Report.edit(submit)
        return self.succ()


if __name__ == "__main__":

    report=Report.add({"schedule":"test","create_time":datetime.now()-timedelta(days=10)})
