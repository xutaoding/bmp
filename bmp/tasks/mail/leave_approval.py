# coding: utf-8

from bmp.const import DEFAULT_GROUP, LEAVE
from bmp.models.user import User, Group
from bmp.models.ref import Ref
from bmp import log
from base import BaseMail


class Mail(BaseMail):
    def to(self, l):
        uids = [l.uid, l.approval_uid] + l.copy_to_uid.split(",")
        if l.status == LEAVE.PASS:
            uids += [u.uid for u in Group.get_users(DEFAULT_GROUP.LEAVE.MAIL)]
            to = [User.get(uid)["mail"] for uid in uids]
            to.append("hr.dept@chinascopefinancial.com")
        else:
            to = [User.get(uid)["mail"] for uid in uids]

        status = l.status
        if status != LEAVE.PASS:
            status = u"已退回"

        sub = u"请假申请%s 编号:%d 申请人:%s 审批时间:%s" % (status, l.id, l.uid,l.approval_time.strftime("%Y-%m-%d"))

        self.send(
            to,
            sub,
            "/templates/leave/approval.html",
            "mail.leave.tpl.html",
            leave=l,
            ref=Ref.map(LEAVE.TYPE))
