# coding=utf-8
import json
from datetime import datetime

from sqlalchemy import or_

from bmp import db
from bmp.apis.base import BaseApi
from bmp.const import ACCESS, DEFAULT_GROUP
from bmp.models.access import Access
from bmp.tasks.mail.access import Mail
from bmp.utils import session
from bmp.utils.exception import ExceptionEx


class AccessApi(BaseApi):
    route = ["/access", "/access/<int:aid>", "/access/<int:page>/<int:pre_page>"]

    # 申请人 申请时间 类型 理由 内容 操作
    def get(self, page=0, pre_page=None, aid=0):
        if aid:
            return self.succ(Access.get(aid))

        filters = [Access.status == ACCESS.NEW]

        if not session.is_admin() and not session.in_group(DEFAULT_GROUP.OP):
            filters.append(Access.apply_uid == session.get_uid())

        return self.succ(Access.select(
            page=page,
            pre_page=pre_page,
            _filters=filters,
            _orders=Access.apply_time.desc()
        ))

    def post(self):
        submit = self.request()
        submit["apply_time"] = datetime.now()
        submit["apply_uid"] = session.get_uid()
        submit["content"] = json.dumps(submit["content"])

        Access.add(submit)
        return self.succ()

    def put(self, aid):
        submit = self.request()
        submit["id"] = aid
        if submit.__contains__("content"):
            submit["content"] = json.dumps(submit["content"])

        access = Access.edit(submit, auto_commit=False)

        if submit["status"] == ACCESS.APPROVAL:
            mail = Mail()
            if not mail.to(access):
                raise ExceptionEx("邮件发送失败")

        db.session.commit()
        return self.succ()

    def delete(self, aid):

        Access.delete(aid)
        return self.succ()


if __name__ == "__main__":
    pass
