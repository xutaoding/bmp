# coding: utf-8
import smtplib
from email.mime.text import MIMEText
from uuid import uuid1
import traceback
from smtplib import SMTPException
from datetime import datetime, timedelta

from bmp import app, log

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor

sched=BlockingScheduler(
        jobstores={
            "default": SQLAlchemyJobStore(url="mysql://ops:Ops@192.168.250.10:3306/bmp_test")
        },
        executors={
            "default": ProcessPoolExecutor(1)
        },
        job_defaults={"coalesce": False, "max_instances": 1}
    )


def __send(sub, html, receiver, copyto, uuid, priority, minutes):
    print("__send %s to %s" % (sub, ";".join(receiver)))

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
        msg.add_header("X-Priority", str(priority))
        smtp.sendmail(app.config["MAIL_DEFAULT_SENDER"], receiver, msg.as_string())
        smtp.close()
    except SMTPException, e:
        traceback.print_exc()
        log.exception(e)
        if minutes < 12:
            minutes += 1
            sched.add_job(__send, "date", run_date=datetime.now() + timedelta(minutes=minutes), id=uuid,
                          args=(sub, html, receiver, copyto, uuid, priority, minutes),replace_existing=True)

def send(sub, html, receiver, copyto=[], date=None, priority="3"):
    uuid = "%s" % (uuid1())
    print("send %s to %s" % (sub, ";".join(receiver)))

    minutes = 1

    run_date = datetime.now() + timedelta(minutes=minutes)
    if date: run_date = date

    sched.add_job(__send, "date", run_date=run_date, id=uuid,
                  args=(sub, html, receiver, copyto, uuid, priority, minutes),replace_existing=True)
    try:
        if not sched.running:
            sched.start()
    except:
        traceback.print_exc()


if __name__ == "__main__":

    send("a" ,"a",["chenglong.yan@chinascopefinancial.com"])
    send("b" ,"b",["chenglong.yan@chinascopefinancial.com"])

    sched.start()