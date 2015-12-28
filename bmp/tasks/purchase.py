# coding: utf-8
import re
import traceback

from flask import render_template
from flask import request

from bmp.models.user import Group, User
import bmp.utils.mail as mail
from bmp import log
from bmp.utils import user_ldap
from bmp.const import PURCHASE
from bmp import sched


def mail_to(p):
    approvals = p.approvals
    to = []
    if not p.is_finished:
        if p.cur_approval_type == PURCHASE.FLOW_ONE:
            suser = User.get(user_ldap.get_superior(p.apply_uid))
            to.append(suser["mail"])
        else:
            to.extend([u.mail for u in Group.get_users(p.cur_approval_type)])
    else:
        user = User.get(p.apply_uid)
        to.extend([u.mail for u in Group.get_users(PURCHASE.FIN)])
        to.append(user["mail"])

    sub = u"采购编号:%s 采购申请:%s" % (p.id,",".join([g.category.name for g in p.goods]))

    regx = re.compile(r"^http://([a-z.]+)/")
    host=regx.findall(request.headers["Referer"])[0]

    if "dev" in host:
        sub=u"【测试】 %s"%sub

    url = "http://%s/templates/purchase/approval.html" % host

    html = render_template(
        "mail.purchase.tpl.html",
        sub=sub,
        purchase=p,
        goods=p.goods,
        approvals=approvals,
        group_names=Group.get_descs(),
        url=url)

    mail.send(sub, html, list(set(to)),priority=1)
