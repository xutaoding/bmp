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
    def to(self, s):
        self.send(
            [app.config["MAIL_ALERT"]],
            u"库存提醒 固定资产 %s 将于 %s 过保" % (s.no, s.warranty_time.strftime("%Y-%m-%d")),
            "/templates/asset/stock.html",
            "mail.stock.tpl.html",
            date=s.warranty_time - timedelta(days=30))
