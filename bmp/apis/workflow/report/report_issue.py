# coding=utf-8
from datetime import datetime

from bmp.apis.base import BaseApi
from bmp.models.report import ReportIssue
from datetime import datetime
from datetime import timedelta


class Report_issueApi(BaseApi):
    route = [
        "/report/issue/<int:rid>",
        "/report/issue"
    ]

    def post(self):
        submit = self.request()
        ReportIssue.add(submit)
        return self.succ()

    def delete(self, rid):
        ReportIssue.delete(rid)
        return self.succ()

    def put(self, rid):
        submit = self.request()
        submit["id"] = rid
        ReportIssue.edit(submit)
        return self.succ()


if __name__ == "__main__":
    pass
    #report=Report.add({"schedule":"test","create_time":datetime.now()})
