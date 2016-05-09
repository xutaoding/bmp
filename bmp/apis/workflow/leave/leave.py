# coding=utf-8
from datetime import datetime

from bmp.apis.base import BaseApi
from bmp.models.leave import Leave
from bmp.tasks.mail.leave import Mail

from flask import session
from bmp.const import USER_SESSION
from datetime import timedelta

from bmp import db
import pandas as pd

from bmp.utils.exception import ExceptionEx


class LeaveApi(BaseApi):
    route = ["/leave", "/leave/<string:begin_time>/<string:end_time>", "/leave/<int:lid>"]

    def get(self, begin_time, end_time):
        return self.succ(Leave.between(begin_time, end_time))

    def post(self):
        submit = self.request()
        submit["uid"] = session[USER_SESSION]["uid"]
        submit["apply_time"] = datetime.now()
        if Leave.check_overlap(submit):
            raise ExceptionEx("起止时间不能与已提交申请重叠,"
                              "可在请假审批中修改已提交的申请")

        leave = Leave.add(submit,auto_commit=False)
        Mail().to(leave)

        db.session.commit()
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
