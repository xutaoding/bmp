# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.const import ACCESS
from bmp.models.access import Access


class Access_historyApi(BaseApi):
    route = ["/access/history"]

    def get(self):
        return self.succ(Access.select(
            _filters=Access.status.in_([ACCESS.FAIL, ACCESS.PASS]))
        )
