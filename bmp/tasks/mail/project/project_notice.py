# coding: utf-8

from bmp.models.user import User
from bmp.tasks.mail.base import BaseMail


class Mail(BaseMail):
    def to(self, p):
        self.send(
            [u.mail for u in User.get_business_category("it")],
            u"【%s】 %s:%s %s" % (p.type, p.txt, p.uid, p.time.strftime("%Y-%m-%d %H:%M:%S")),
            "/templates/project/index.html",
            "mail.project_notice.tpl.html")
