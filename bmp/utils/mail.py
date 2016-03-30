# coding: utf-8
import smtplib
from email.mime.text import MIMEText
from bmp import app
import email


def send(sub, html, receiver, copyto=None, priority="3"):
    print("send %s to %s" % (sub, ";".join(receiver)))

    msg = MIMEText(html, _subtype="html", _charset="utf-8")
    msg["Subject"] = sub
    msg["From"] = app.config["MAIL_DEFAULT_SENDER"]
    msg["To"] = ";".join(receiver)
    msg["Date"] = email.utils.formatdate(localtime=True)

    if copyto:
        msg["Cc"] = ";".join(copyto)

    smtp = smtplib.SMTP()
    smtp.connect(app.config["MAIL_SERVER"])
    smtp.login(app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
    msg.add_header("X-Priority", str(priority))
    smtp.sendmail(app.config["MAIL_DEFAULT_SENDER"], receiver, msg.as_string())
    smtp.close()


if __name__ == "__main__":
    send("test","<html><title></title><body></body></html>",["chenglong.yan@chinascopefinancial.com"])
