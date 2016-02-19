# coding: utf-8

from bmp import log
from bmp.models.user import Group, User
from bmp.const import RELEASE, DEFAULT_GROUP
from bmp.tasks.mail.base import BaseMail

class Mail(BaseMail):
    def to(self, r,submit):
        approvals = r.approvals
        to, cc = [], []
        to_group = [DEFAULT_GROUP.QA]
        to_group.extend([DEFAULT_GROUP.OP])
        for g in to_group:
            to.extend([u.mail for u in Group.get_users(g)])

        user = User.get(r.apply_uid)
        sub = u"发布申请:%s" % r.project
        if submit and submit["status"] == RELEASE.FAIL:
            sub = u"发布退回:%s %s" % (r.project, submit["type"])
            to = [user["mail"]]
        elif approvals:
            sub = u"发布确认:%s %s" % (r.project, submit["type"])
            to.append(user["mail"])

        try:
            copy_to = User.get(r.copy_to_uid)
            if copy_to["mail"] not in to:
                cc.append(copy_to["mail"])
        except:
            pass

        self.send(
            to,
            sub,
            "/templates/release/release.html",
            "mail.tpl.html",
            cc=cc,
            release=r,
            approvals=approvals)


