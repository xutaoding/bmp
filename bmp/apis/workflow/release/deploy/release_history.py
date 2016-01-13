# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.release import Release


class Release_historyApi(BaseApi):
    route = ["/release/deploy/history/<int:page>/<int:pre_page>"]

    def get(self, page=0, pre_page=None):
        return self.succ(Release.deployed(page, pre_page))


if __name__ == "__main__":
    pass
