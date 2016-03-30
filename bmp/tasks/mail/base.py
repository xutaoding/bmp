# coding: utf-8
from flask import render_template
import bmp.utils.mail as mail
import re
from flask import request


class BaseMail:
    def __init__(self):
        pass

    def send(self, to, sub, url, tpl, cc=[], date=None, **kwargs):
        regx = re.compile(r"^http://([a-z.]+)/")
        host = regx.findall(request.headers["Referer"])[0]

        if "dev" in host: sub = u"【测试】 %s" % sub

        kwargs["url"] = "http://%s%s" % (host, url)
        kwargs["sub"] = sub

        html = render_template(tpl, **kwargs)

        mail.send(sub, html, list(set(to)), cc, date)
