# coding: utf-8
from datetime import timedelta
from bmp import app

from bmp.tasks.mail.base import BaseMail

class Mail(BaseMail):
    def to(self, c):
        def __send(days):
            self.send(
                [app.config["MAIL_ALERT"]],
                u"合同提醒 %s 将于 %s 结束" % (c.desc, c.end_time.strftime("%Y-%m-%d")),
                "/templates/asset/contract.html",
                "mail.contract.tpl.html",
                date=c.end_time - timedelta(days=days))
        __send(30)
        __send(60)
