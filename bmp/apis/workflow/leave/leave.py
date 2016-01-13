# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.leave import Leave


class LeaveApi(BaseApi):
    route = ["/leave", "/leave/<int:page>/<int:pre_page>", "/leave/<int:lid>"]

    def get(self, page, pre_page):
        return self.succ(Leave.select(page, pre_page))

    def post(self):
        submit = self.request()
        Leave.add(submit)
        return self.succ()

    def delete(self, lid):
        Leave.delete(lid)
        return self.succ()


if __name__ == "__main__":
    pass
