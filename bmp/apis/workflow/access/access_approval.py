# coding=utf-8
from datetime import datetime

from bmp.apis.base import BaseApi
from bmp.const import ACCESS
from bmp.models.access import Access
from bmp.utils.exception import ExceptionEx
from flask import session
from bmp.const import USER_SESSION


class Access_approvalApi(BaseApi):
    route = ["/access/approval/<int:aid>", "/access/approval/<int:page>/<int:pre_page>"]

    # 申请人 申请时间 类型 理由 内容 操作
    def get(self, page=0, pre_page=None):
        return self.succ(Access.select(
            page=page,
            pre_page=pre_page,
            _filters=Access.status == ACCESS.APPROVAL
        ))

    def put(self, aid):
        submit = self.request()
        access = Access.get(aid)
        if access["status"] != ACCESS.APPROVAL:
            raise ExceptionEx("申请未提交")

        submit["approval_uid"] = session[USER_SESSION]["uid"]
        submit["approval_time"] = datetime.now()
        submit["id"] = aid
        Access.edit(submit)
        return self.succ()
