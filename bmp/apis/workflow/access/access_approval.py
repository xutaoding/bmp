# coding=utf-8
from datetime import datetime

from bmp.apis.base import BaseApi
from bmp.models.access import Access


class Access_approvalApi(BaseApi):
    route = ["/access/approval/<int:aid>"]

    def put(self, aid):
        submit = self.request()
        submit["approval_time"] = datetime.now()
        submit["id"] = aid
        Access.edit(submit)
        return self.succ()
