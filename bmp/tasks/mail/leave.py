# coding: utf-8

from bmp.const import DEFAULT_GROUP, LEAVE
from bmp.models.user import User, Group
from bmp.models.ref import Ref
from bmp import log
from base import BaseMail


class Mail(BaseMail):
    def to(self, l):
        uids = [l.approval_uid] + l.copy_to_uid.split(",")
        to = [User.get(uid)["mail"] for uid in uids]

        sub = u"请假申请 编号:%d 申请人:%s" % (l.id, l.uid)

        self.send(
            to,
            sub,
            "/templates/leave/approval.html",
            "mail.leave.tpl.html",
            leave=l,
            ref=Ref.map(LEAVE.TYPE))



