# coding: utf-8

from bmp.const import DEFAULT_GROUP, LEAVE
from bmp.models.user import User, Group
from bmp.models.ref import Ref
from bmp import log
from base import BaseMail
from bmp.utils.exception import ExceptionEx


class Mail(BaseMail):
    def to(self, l):
        try:
            uids = [l.approval_uid] + l.copy_to_uid.split(",")
            to = [User.get(uid)["mail"] for uid in uids]

            sub = u"请假申请 申请人:%s 申请时间:%s 编号:%d" % (l.uid,l.apply_time.strftime("%Y-%m-%d"),l.id)

            self.send(
                to,
                sub,
                "/templates/leave/approval.html",
                "mail.leave.tpl.html",
                leave=l,
                ref=Ref.map(LEAVE.TYPE))
        except:
            raise ExceptionEx("邮件发送失败,请重试!")



