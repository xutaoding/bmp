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

            sub = u"%s的请假申请%s 审批时间:%s 编号:%d" % ( l.uid,status,l.approval_time.strftime("%Y-%m-%d"),l.id)

            self.send(
                to,
                sub,
                "/templates/leave/approval.html",
                "mail.leave.tpl.html",
                leave=l,
                leave_type=Ref.map(LEAVE.TYPE)[int(l.type_id)])

        except Exception,e:
            log.exception(e)
            raise ExceptionEx("邮件发送失败,请重试!")
