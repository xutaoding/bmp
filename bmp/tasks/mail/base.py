# coding: utf-8
import re

from flask import render_template
from flask import request

import bmp.utils.mail as mail
from bmp import log
from bmp.tasks.base import BaseTask


class BaseMail(BaseTask):
    def send(self, to, sub, url, tpl, cc=[], date=None, _id=None, **kwargs):
        regx = re.compile(r"^http://([a-z.]+)/")
        host = regx.findall(request.headers["Referer"])[0] if request.headers.__contains__("Referer") else ""

        if "dev" in host: sub = u"【测试】 %s" % sub

        kwargs["url"] = "http://%s%s" % (host, url)
        kwargs["sub"] = sub

        html = render_template(tpl, **kwargs)

        to = list(set(to))

        if _id:
            log.info("mailto %s %s _id" % (";".join(to), sub))
            self.add_job(mail.send, (sub, html, to, cc, 3), date, _id="_".join(["mail", _id]))
        else:
            log.info("mailto %s %s" % (";".join(to), sub))
            self.add_job(mail.send, (sub, html, to, cc, 3), date)

    def remove(self, _id):
        _id = "_".join(["mail", _id])
        self.remove_job(_id)


if __name__ == "__main__":
    pass
