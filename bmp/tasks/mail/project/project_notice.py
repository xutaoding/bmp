# coding: utf-8
import re

from flask import render_template
from flask import request

import bmp.utils.mail as mail
from bmp.models.user import User


def mail_to(p):
    sub = u"【%s】 %s:%s %s" % (p.type,p.txt,p.uid,p.time.strftime("%Y-%m-%d %H:%M:%S"))

    regx = re.compile(r"^http://([a-z.]+)/")

    host = regx.findall(request.headers["Referer"])[0]

    if "dev" in host:
        sub = u"【测试】 %s" % sub

    url = "http://%s/templates/project/index.html"%host

    html = render_template(
        "mail.project_notice.tpl.html",
        sub=sub,
        url=url)

    mail.send(sub, html,
              receiver=[u.mail for u in User.get_business_category("it")])
