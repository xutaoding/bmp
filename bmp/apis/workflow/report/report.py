# coding=utf-8
from datetime import datetime

from bmp.apis.base import BaseApi
from bmp.models.report import Report
from datetime import datetime
from datetime import timedelta
from bmp.utils.exception import ExceptionEx
from bmp.models.report import ReportTeam


class ReportApi(BaseApi):
    route = [
        "/report",
        "/report/<int:year>/<int:weeks>",
        "/report/<int:year>/<int:weeks>/<int:team_id>",
        "/report/<int:rid>"
    ]

    def get(self, year, weeks, team_id=None):
        dt = datetime(year, 1, 1) + timedelta(weeks=weeks - 1)
        beg_time = dt - timedelta(days=dt.weekday())
        end_time = (dt + timedelta(days=6 - dt.weekday())).replace(hour=23, minute=59, second=59)
        if team_id:
            result = Report.select(
                _filters=[Report.create_time.between(beg_time, end_time), Report.team_id == team_id])
        else:
            result = Report.select(
                _filters=[Report.create_time.between(beg_time, end_time),ReportTeam.is_del!=True],_joins=ReportTeam)

        return self.succ(result)

    def post(self):
        submit = self.request()

        if not submit.__contains__("create_time"):
            submit["create_time"] = datetime.now()
        else:
            submit["create_time"] = datetime.strptime(submit["create_time"], "%Y-%m-%d")

        beg_time = (submit["create_time"] - timedelta(days=submit["create_time"].weekday())).replace(hour=0, minute=0,
                                                                                                     second=0)
        end_time = (submit["create_time"] + timedelta(days=6 - submit["create_time"].weekday())).replace(hour=23,
                                                                                                         minute=59,
                                                                                                         second=59)

        if Report.query.filter(Report.create_time.between(beg_time, end_time)) \
                .filter(Report.team_id == submit["team_id"]).count():
            raise ExceptionEx("本周计划已添加")

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
    Report.add({"create_time": ""})
