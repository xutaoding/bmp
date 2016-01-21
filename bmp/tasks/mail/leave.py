# coding: utf-8
import re

from flask import render_template
from flask import request

import bmp.utils.mail as mail
from bmp.const import DEFAULT_GROUP, LEAVE
from bmp.models.user import User, Group
from bmp.models.ref import Ref
from bmp import log


def mail_to(l):
    try:
        uids = [u.uid for u in Group.get_users(DEFAULT_GROUP.HR)] + [l.approval_uid]
        to = [User.get(uid)["mail"] for uid in uids]

        sub = u"请假申请 编号:%d 申请人:%s" % (l.id, l.uid)

        regx = re.compile(r"^http://([a-z.]+)/")
        host = regx.findall(request.headers["Referer"])[0]

        if "dev" in host: sub = u"【测试】 %s" % sub

        url = "http://%s/templates/leave/approval.html" % host

        html = render_template(
            "mail.leave.tpl.html",
            sub=sub,
            leave=l,
            ref=Ref.map(LEAVE.TYPE),
            url=url)

        mail.send(sub, html, list(set(to)))
    except Exception, e:
        log.exception(e)


if __name__ == "__main__":
    pass
