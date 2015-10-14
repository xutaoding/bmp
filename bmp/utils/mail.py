#!/usr/bin/env python3
#coding: utf-8
from bmp import app
import smtplib
from email.mime.text import MIMEText


def send(receiver,sub,html):
    msg = MIMEText(html,_subtype="html",_charset="utf-8")
    msg["Subject"] = sub
    msg["From"]=app.config["MAIL_DEFAULT_SENDER"]
    msg["To"]=";".join(receiver)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(app.config["MAIL_SERVER"])
        smtp.login(app.config["MAIL_USERNAME"],app.config["MAIL_PASSWORD"])
        smtp.sendmail(app.config["MAIL_DEFAULT_SENDER"], receiver,msg.as_string())
        smtp.close()
        return True
    except:
        return False


if __name__=="__main__":
    send(["chenglong.yan@chinascopefinancial.com"],"test","test")