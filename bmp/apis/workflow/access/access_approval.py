# coding=utf-8
from datetime import datetime
from operator import or_

from bmp.apis.base import BaseApi
from bmp.const import ACCESS,DEFAULT_GROUP, USER_SESSION
from bmp.models.access import Access
from bmp.utils import session
from bmp.utils.exception import ExceptionEx


class Access_approvalApi(BaseApi):
    route = ["/access/approval/<int:aid>", "/access/approval/<int:page>/<int:pre_page>"]

    # 申请人 申请时间 类型 理由 内容 操作
    def get(self, page=0, pre_page=None):
        filters = [Access.status == ACCESS.APPROVAL]

        if not session.is_admin() and not session.in_group(DEFAULT_GROUP.OP):
            filters.append(or_(
                Access.apply_uid == session.get_uid(),
                Access.copy_to_uid.like("%" + session.get_uid() + "%")
            ))

        return self.succ(Access.select(
            page=page,
            pre_page=pre_page,
            _filters=filters,
            _orders=Access.apply_time.desc()
        ))

    def put(self, aid):
        submit = self.request()
        access = Access.get(aid)
        if access["status"] != ACCESS.APPROVAL:
            raise ExceptionEx("申请未提交")

        submit["approval_uid"] = session.get_uid()
        submit["approval_time"] = datetime.now()
        submit["id"] = aid
        Access.edit(submit)
        return self.succ()
