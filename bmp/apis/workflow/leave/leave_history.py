# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.leave import Leave


class Leave_historyApi(BaseApi):
    route = ["/leave/history/<int:page>/<int:pre_page>"]

    def get(self, page, pre_page):
        return self.succ(Leave.history(page, pre_page))


if __name__ == "__main__":
    print Leave.history(1,10)
