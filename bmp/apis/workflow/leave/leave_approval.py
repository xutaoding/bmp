# coding=utf-8
from datetime import datetime

from bmp import db
from bmp.apis.base import BaseApi
from bmp.models.leave import Leave
from bmp.tasks.mail.leave_approval import Mail


class Leave_approvalApi(BaseApi):
    route = ["/leave/approval/<int:lid>", "/leave/approval/<int:page>/<int:pre_page>"]

    def get(self, page, pre_page):
        return self.succ(Leave.unapprovaled(page, pre_page))

    def put(self, lid):
        submit = self.request()
        submit["id"] = lid
        submit["approval_time"] = datetime.now().strftime("%Y-%m-%d")
        leave = Leave.edit(submit, auto_commit=False)
        Mail().to(leave)

        db.session.commit()
        return self.succ()


if __name__ == "__main__":
    pass
