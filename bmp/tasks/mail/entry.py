# coding: utf-8

from base import BaseMail
from bmp import log
from bmp.utils.exception import ExceptionEx
from bmp import app

class Mail(BaseMail):
    def to(self, user):
        try:

            sub = u"入职提醒 用户名:%s 密码:%s" % (user["uid"], user["userPassword"])

            self.send(
                [app.config["MAIL_ALERT"]],
                sub,
                "",
                "mail.alert.tpl.html")

            return True
        except Exception, e:
            return False
