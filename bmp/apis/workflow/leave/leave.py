# coding=utf-8
from datetime import datetime

from bmp.apis.base import BaseApi
from bmp.models.leave import Leave
from bmp.tasks.mail.leave import Mail


class LeaveApi(BaseApi):
    route = ["/leave", "/leave/<string:begin_time>/<string:end_time>", "/leave/<int:lid>"]

    def get(self, begin_time, end_time):
        return self.succ(
            Leave.between(datetime.strptime(begin_time, "%Y-%m-%d"),
                          datetime.strptime(end_time, "%Y-%m-%d"))
        )

    def post(self):
        submit = self.request()
        leave = Leave.add(submit)
        Mail().to(leave)
        return self.succ()

    def delete(self, lid):
        Leave.delete(lid)
        return self.succ()


if __name__ == "__main__":
    pass
