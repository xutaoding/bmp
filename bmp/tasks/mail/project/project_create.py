# coding: utf-8

from bmp import log
from bmp.models.user import User
from bmp.tasks.mail.base import BaseMail


class Mail(BaseMail):
    def to(self, p):
        self.send(
            [User.get(u)["mail"] for u in [p.demand_uid, p.develop_uid, p.test_uid, p.release_uid]],
            u"项目创建提醒: %s" % (p.name),
            "/templates/project/edit.html?id=%d"%p.id,
            "mail.project.tpl.html")


