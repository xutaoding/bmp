# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.leave import LeaveEvent


class Leave_eventApi(BaseApi):
    route = ["/leave/event", "/leave/event/<int:page>/<int:pre_page>", "/leave/event/<int:lid>"]

    def get(self, page, pre_page):
        return self.succ(LeaveEvent.select(page, pre_page))

    def post(self):
        submit = self.request()
        LeaveEvent.add(submit)
        return self.succ()

    def delete(self, lid):
        LeaveEvent.delete(lid)
        return self.succ()


if __name__ == "__main__":
    pass
