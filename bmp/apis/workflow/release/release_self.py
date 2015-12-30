# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.release import Release


class Release_selfApi(BaseApi):
    route = ["/release/self/<int:page>/<int:pre_page>"]

    def get(self,page=0, pre_page=None):
        return self.succ(Release.self(page,pre_page))


if __name__ == "__main__":
    pass
