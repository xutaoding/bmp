# coding: utf-8

from bmp import log
import traceback
from bmp.models.user import Group, User
from bmp.utils.user_ldap import Ldap
from bmp.const import PURCHASE,DEFAULT_GROUP
from base import BaseMail

class Mail(BaseMail):
    def to(self, p):
        approvals = p.approvals
        to = []
        if not p.is_finished:
            if p.cur_approval_type == PURCHASE.FLOW_ONE:
                ldap=Ldap()
                suser = User.get(ldap.get_superior(p.apply_uid))
                to.append(suser["mail"])
            else:
                to.extend([u.mail for u in Group.get_users(p.cur_approval_type)])
        else:
            user = User.get(p.apply_uid)
            to.extend([u.mail for u in Group.get_users(DEFAULT_GROUP.PURCHASE.FIN)])
            to.append(user["mail"])

        sub = u"采购编号:%s 采购申请:%s" % (p.id, ",".join([g.category.name for g in p.goods]))

        self.send(
            to,
            sub,
            "/templates/purchase/approval.html",
            "mail.purchase.tpl.html",
            purchase=p,
            goods=p.goods,
            approvals=approvals,
            group_names=Group.get_descs())



