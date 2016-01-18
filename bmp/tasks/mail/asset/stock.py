# coding: utf-8
import re
from datetime import timedelta
import traceback

from flask import render_template
from flask import request

import bmp.utils.mail as mail
from bmp import app


def mail_to(s):
    try:
        sub = u"库存提醒 固定资产 %s 将于 %s 过保" % (s.no, s.warranty_time.strftime("%Y-%m-%d"))

        regx = re.compile(r"^http://([a-z.]+)/")

        host = regx.findall(request.headers["Referer"])[0]

        if "dev" in host:
            sub = u"【测试】 %s" % sub

        url = "http://%s/templates/asset/stock.html" % host

        html = render_template(
            "mail.stock.tpl.html",
            sub=sub,
            url=url)

        mail.send(sub, html, receiver=[app.config["MAIL_ALERT"]], date=s.warranty_time - timedelta(days=30))
    except:
        traceback.print_exc()


if __name__ == "__main__":
    pass
