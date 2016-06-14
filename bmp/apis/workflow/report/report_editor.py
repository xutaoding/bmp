# coding=utf-8

from flask import session

from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION
from bmp.models.report import ReportEditor, ReportTeam
from bmp.utils.exception import ExceptionEx


class Report_editorApi(BaseApi):
    route = ["/report/editor/<int:tid>", "/report/editor/<int:tid>/<int:eid>"]

    def post(self, tid):
        submit = self.request()
        team = ReportTeam.get(tid)
        if session[USER_SESSION]["uid"] != team["create_uid"]:
            raise ExceptionEx("当前用户无法新建编辑人")

        submit["team_id"] = tid

        ReportEditor.add(submit)
        return self.succ()

    def delete(self, tid, eid):
        team = ReportTeam.get(tid)
        if session[USER_SESSION]["uid"] != team["create_uid"]:
            raise ExceptionEx("当前用户无法删除编辑人")


        ReportEditor.delete(eid)
        return self.succ()

