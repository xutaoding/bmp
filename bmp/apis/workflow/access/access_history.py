# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.const import ACCESS
from bmp.models.access import Access


class Access_historyApi(BaseApi):
    route = ["/access/history/<int:page>/<int:pre_page>"]

    # 申请人 申请时间 类型 理由 内容 操作
    def get(self, page=0, pre_page=None):
        return self.succ(Access.select(
            page=page,
            pre_page=pre_page,
            _filters=Access.status.in_([ACCESS.FAIL, ACCESS.DEPLOY])
        ))
