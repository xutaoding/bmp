# coding: utf-8
import re
import traceback

from flask import render_template
from flask import request

import bmp.utils.mail as mail

from bmp.models.leave import Leave

from bmp.models.user import User


def mail_to(l):
    try:

        to=[User.get(l.approval_uid)["mail"]]

        sub = u"请假申请 编号:%d 申请人:%s 天数:%d" % (l.id,l.uid,l.days)

        regx = re.compile(r"^http://([a-z.]+)/")
        host = regx.findall(request.headers["Referer"])[0]

        if "dev" in host:
            sub = u"【测试】 %s" % sub

        url = "http://%s/templates/leave/approval.html" % host

        html = render_template(
            "mail.leave.tpl.html",
            sub=sub,
            url=url)

        mail.send(sub, html, list(set(to)))
    except:
        traceback.print_exc()
