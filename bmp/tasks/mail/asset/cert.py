# coding: utf-8
import re
from datetime import timedelta
import traceback

from flask import render_template
from flask import request

import bmp.utils.mail as mail
from bmp import app


from bmp.tasks.mail.base import BaseMail

class Mail(BaseMail):
    def to(self, c):
        self.send(
            [app.config["MAIL_ALERT"]],
            u"证书提醒 %s 将于 %s 到期" % (c.name, c.end_time.strftime("%Y-%m-%d")),
            "/templates/asset/ssl.html",
            "mail.cert.tpl.html",
            date=c.end_time - timedelta(days=20))
