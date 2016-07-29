# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.access import AccessDeployHistory


class Access_deploy_historyApi(BaseApi):
    route = ["/access/deploy/history",
             "/access/deploy/history/<int:page>/<int:pre_page>",
             "/access/deploy/history/<int:hid>"]

    def get(self, page=None, pre_page=None, hid=None):
        if hid:
            return self.succ(AccessDeployHistory.get(hid))
        return self.succ(AccessDeployHistory.select(
            page,
            pre_page
        ))
