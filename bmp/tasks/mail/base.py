# coding: utf-8
from flask import render_template
import bmp.utils.mail as mail
import re
from flask import request
from bmp.tasks.base import BaseTask


class BaseMail(BaseTask):
    def send(self, to, sub, url, tpl, cc=[], date=None, _id=None, **kwargs):
        regx = re.compile(r"^http://([a-z.]+)/")
        host = regx.findall(request.headers["Referer"])[0]

        if "dev" in host: sub = u"【测试】 %s" % sub

        kwargs["url"] = "http://%s%s" % (host, url)
        kwargs["sub"] = sub

        html = render_template(tpl, **kwargs)

        if _id:
            self.add_job(mail.send, (sub, html, list(set(to)), cc, 3), date, _id="_".join(["mail", _id]))
        else:
            self.add_job(mail.send, (sub, html, list(set(to)), cc, 3), date)

    def remove(self,_id):
        _id="_".join(["mail", _id])
        self.remove_job(_id)

if __name__ == "__main__":
    pass

