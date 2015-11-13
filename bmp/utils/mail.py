#!/usr/bin/env python3
# coding: utf-8
from bmp import app, log
import smtplib
from email.mime.text import MIMEText
import threading
import traceback

#todo 数据库中增加待发邮件表,此处只做待发邮件的添加,后续由发件协程处理
def send(sub, html, receiver, copyto=[]):
    def __send(sub, html, receiver, copyto):
        msg = MIMEText(html, _subtype="html", _charset="utf-8")
        msg["Subject"] = sub
        msg["From"] = app.config["MAIL_DEFAULT_SENDER"]
        msg["To"] = ";".join(receiver)
        if copyto:
            msg["Cc"] = ";".join(copyto)
        try:
            smtp = smtplib.SMTP()
            smtp.connect(app.config["MAIL_SERVER"])
            smtp.login(app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            smtp.sendmail(app.config["MAIL_DEFAULT_SENDER"], receiver, msg.as_string())
            smtp.close()
        except Exception, e:
            traceback.print_exc()
            log.exception(e)

    t = threading.Thread(target=__send, args=(sub, html, receiver, copyto))
    t.start()


if __name__ == "__main__":
    send("x", "x", ["chenglong.yan@chinascopefinancial.com"])
