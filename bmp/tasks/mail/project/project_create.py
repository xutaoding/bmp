# coding: utf-8
import re

from flask import render_template
from flask import request

import bmp.utils.mail as mail
from bmp.models.user import User


def mail_to(p):

    sub = u"项目创建提醒: %s" % (p.name)

    regx = re.compile(r"^http://([a-z.]+)/")

    host = regx.findall(request.headers["Referer"])[0]

    if "dev" in host:
        sub = u"【测试】 %s" % sub

    url = "http://%s/templates/project/edit.html?id=%d" % (host, p.id)

    html = render_template(
        "mail.project.tpl.html",
        sub=sub,
        url=url)

    mail.send(sub, html,
              receiver=[User.get(u)["mail"] for u in [p.demand_uid, p.develop_uid, p.test_uid, p.release_uid]])
