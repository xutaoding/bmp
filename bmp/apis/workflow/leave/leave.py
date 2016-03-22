# coding=utf-8
from datetime import datetime

from bmp.apis.base import BaseApi
from bmp.models.leave import Leave
from bmp.tasks.mail.leave import Mail

from flask import session
from bmp.const import USER_SESSION
from datetime import timedelta


class LeaveApi(BaseApi):
    route = ["/leave", "/leave/<string:begin_time>/<string:end_time>", "/leave/<int:lid>"]

    def get(self, begin_time, end_time):
        return self.succ(Leave.between(begin_time, end_time))

    def post(self):
        submit = self.request()
        submit["uid"] = session[USER_SESSION]["uid"]
        submit["apply_time"] = datetime.now()

        leave = Leave.add(submit)
        Mail().to(leave)
        return self.succ()

    def delete(self, lid):
        Leave.delete(lid)
        return self.succ()

    def put(self, lid):
        submit = self.request()
        submit["id"] = lid

        Leave.edit(submit)
        return self.succ()


if __name__ == "__main__":
    pass
