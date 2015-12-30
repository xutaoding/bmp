# coding: utf-8
import re

from flask import render_template
from flask import request

import bmp.utils.mail as mail
from bmp import app
from datetime import timedelta


def mail_to(c):
    sub = u"合同提醒 %s 将于 %s 结束" % (c.desc,c.end_time.strftime("%Y-%m-%d"))

    regx = re.compile(r"^http://([a-z.]+)/")

    host=regx.findall(request.headers["Referer"])[0]

    if "dev" in host:
        sub=u"【测试】 %s"%sub

    url = "http://%s/templates/asset/contract.html" % host

    html = render_template(
        "mail.contract.tpl.html",
        sub=sub,
        url=url)

    mail.send(sub, html,receiver=[app.config["MAIL_ALERT"]],date=c.end_time-timedelta(days=30))
    mail.send(sub, html,receiver=[app.config["MAIL_ALERT"]],date=c.end_time-timedelta(days=60))