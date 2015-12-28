
# coding: utf-8
import re
import traceback
import sys

import bmp.utils.mail as mail

from flask import render_template
from datetime import timedelta
from bmp.utils import time
from bmp import app,sched
from bmp.models.asset import Contract,Stock
from datetime import datetime

def __run():
    with app.app_context():
        def delta(dt,days):
            days=(dt-timedelta(days=days)-datetime.now()).days
            return days

        for contract in Contract.query.all():
            if not (delta(contract.end_time,30) and delta(contract.end_time,60)):
                alert_contract(contract)

        for stock in Stock.query.all():
            if not delta(stock.warranty_time,30):
                alert_stock(stock)


def run():
    try:
        sched.add_job(run,"interval",id="tasks.alert", days=1,replace_existing=True)
        if not sched.running:
            sched.start()
    except:
        pass

def alert_stock(s):
    try:
        sub = u"库存提醒 固定资产 %s 将于 %s 过保" % (s.no,time.format(s.warranty_time,"%Y-%m-%d"))

        regx = re.compile(r"^http://([a-z.]+)/")

        host=regx.findall(app.config["DOMAIN"])[0]

        if "dev" in host:
            sub=u"【测试】 %s"%sub

        url = "http://%s/templates/asset/stock.html" % host

        html = render_template(
            "mail.stock.tpl.html",
            sub=sub,
            url=url)

        mail.send(sub, html,receiver=[app.config["MAIL_ALERT"]])

    except:
        traceback.print_exc()

def alert_contract(c):
    print("alert_contract")
    sub = u"合同提醒 %s 将于 %s 结束" % (c.desc,time.format(c.end_time,"%Y-%m-%d"))

    regx = re.compile(r"^http://([a-z.]+)/")

    host=regx.findall(app.config["DOMAIN"])[0]

    if "dev" in host:
        sub=u"【测试】 %s"%sub

    url = "http://%s/templates/asset/contract.html" % host

    html = render_template(
        "mail.contract.tpl.html",
        sub=sub,
        url=url)

    mail.send(sub, html,receiver=[app.config["MAIL_ALERT"]])


if __name__=="__main__":
    if not sched.get_job("tasks.alert"):
            sched.add_job(run,"interval",id="tasks.alert", days=1)
    try:
        sched.start()
    except:
        sched.shutdown()