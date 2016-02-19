# coding: utf-8

from bmp.const import DEFAULT_GROUP, LEAVE
from bmp.models.user import User, Group
from bmp.models.ref import Ref
from bmp import log
from base import BaseMail


class Mail(BaseMail):
    def to(self, l,copy_to_uid):
        uids = [u.uid for u in Group.get_users(DEFAULT_GROUP.LEAVE_MAIL)] + [l.approval_uid] + copy_to_uid.split(",")
        to = [User.get(uid)["mail"] for uid in uids]
        to.append("hr.dept@chinascopefinancial.com")

        sub = u"请假申请 编号:%d 申请人:%s" % (l.id, l.uid)

        self.send(
            to,
            sub,
            "/templates/leave/approval.html",
            "mail.leave.tpl.html",
            leave=l,
            ref=Ref.map(LEAVE.TYPE))



