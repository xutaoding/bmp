# coding: utf-8
from datetime import timedelta
from bmp import app
from bmp.tasks.mail.base import BaseMail

class Mail(BaseMail):
    def to(self, d):
        self.send(
            [app.config["MAIL_ALERT"]],
            u"域名提醒 %s 将于 %s 到期" % (d.name, d.end_time.strftime("%Y-%m-%d")),
            "/templates/asset/domain.html",
            "mail.domain.tpl.html",
            date=d.end_time - timedelta(days=20))
