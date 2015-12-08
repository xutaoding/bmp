# coding: utf-8
from bmp.models.user import Group, User
from flask import render_template
import bmp.utils.mail as mail
from flask import request
import re
from bmp.const import RELEASE, DEFAULT_GROUP
import traceback
from bmp import log
from flask import session
from bmp.utils import user_ldap
from bmp.const import PURCHASE

def mail_to(p):
    try:
        __mail_to(p)
    except Exception, e:
        traceback.print_exc()
        log.exception(e)


def __mail_to(p):
    approvals = p.approvals
    to=[]
    if not p.is_finished:
        if p.cur_approval_type==PURCHASE.FLOW_ONE:
            suser=User.get(user_ldap.get_superior(p.apply_uid))
            to.append(suser["mail"])
        else:
            to.extend([u.mail for u in Group.get_users(p.cur_approval_type)])
    else:
        user=User.get(p.apply_uid)
        to.extend([u.mail for u in Group.get_users(PURCHASE.FIN)])
        to.append(user["mail"])


    sub = u"采购申请:%s" % ",".join([g.category.name for g in p.goods])

    regx = re.compile(r"^http://([a-z.]+)/")
    url ="http://%s/templates/purchase/approval.html"%regx.findall(request.headers["Referer"])[0]

    html = render_template(
        "mail.purchase.tpl.html",
        sub=sub,
        purchase=p,
        goods=p.goods,
        approvals=approvals,
        group_names=PURCHASE.GROUP_NAMES,
        url=url)

    mail.send(sub, html, list(set(to)))
