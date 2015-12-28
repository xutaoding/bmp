#!/usr/bin/env python3
# coding: utf-8
import smtplib
from email.mime.text import MIMEText
import threading
import traceback
from datetime import date
from bmp import db,app,log
from bmp import sched
from uuid import uuid1
import traceback

def __send(sub,html,receiver,copyto,uuid):
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
            sched.remove_job(uuid)
            smtp.close()
        except Exception, e:
            traceback.print_exc()
            log.exception(e)

def send(sub, html, receiver,copyto=[],date=None):
    uuid="%s%s"%(sub,uuid1())
    print("send %s to %s"%(sub,";".join(receiver)))

    if date:
        sched.add_job(__send,"date",run_date=date,id=uuid,args=(sub,html,receiver,copyto,uuid))
    else:
        sched.add_job(__send,"interval", minutes=1,id=uuid,args=(sub,html,receiver,copyto,uuid))
    try:
        if not sched.running:
            sched.start()
    except:
        traceback.print_exc()

if __name__ == "__main__":
    send("x", "x", ["chenglong.yan@chinascopefinancial.com"])
