# coding: utf-8

from datetime import datetime

from base import BaseMail
from bmp import log
from bmp.const import LEAVE
from bmp.models.ref import Ref
from bmp.models.user import User
from bmp.utils.exception import ExceptionEx


class Mail(BaseMail):
    def to(self, uid, newpass):
        try:
            user = User.get(uid)
            sub = u"密码重置提醒 %s" % (datetime.now().strftime("%Y-%m-%d %M:%S"))

            self.send(
                [user["mail"]],
                sub,
                "",
                "mail.passwd.tpl.html",
                newpass=newpass,
            )
        except Exception, e:
            log.exception(e)
            raise ExceptionEx("邮件发送失败,请重试!")


if __name__ == "__main__":
    print Ref.map(LEAVE.TYPE)[77]
