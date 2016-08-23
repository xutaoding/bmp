# coding: utf-8

from datetime import datetime

from base import BaseMail
from bmp import app


class Mail(BaseMail):
    def to(self, user):
        try:

            sub = u"入职通知 %s" % datetime.now().strftime("%Y-%m-%d %H:%M")

            self.send(
                [app.config["MAIL_ALERT"], user["mail"]],
                sub,
                "",
                "mail.entry.tpl.html", uid=user["uid"], pwd=user["pwd"])

            return True
        except Exception, e:
            return False
