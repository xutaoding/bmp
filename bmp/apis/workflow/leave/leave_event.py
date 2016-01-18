# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.leave import LeaveEvent
from datetime import datetime

class Leave_eventApi(BaseApi):
    route = ["/leave/event", "/leave/event/<string:begin_time>/<string:end_time>", "/leave/event/<int:lid>"]

    def get(self, begin_time, end_time):
        return self.succ(
            LeaveEvent.between(datetime.strptime(begin_time, "%Y-%m-%d"),
                          datetime.strptime(end_time, "%Y-%m-%d"))
        )

    def post(self):
        submit = self.request()
        LeaveEvent.add(submit)
        return self.succ()

    def delete(self, lid):
        LeaveEvent.delete(lid)
        return self.succ()


if __name__ == "__main__":
    pass
