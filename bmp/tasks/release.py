#coding: utf-8
from bmp.models.user import Group,User
from flask import render_template
import bmp.utils.mail as mail
from flask import request
import re
from bmp.const import RELEASE,DEFAULT_GROUP
import traceback
from bmp import log

def mail_to(r,submit=None):
    try:
        __mail_to(r,submit)
    except Exception,e:
        traceback.print_exc()
        log.exception(e)

def __mail_to(r,submit):
    approvals=r.approvals

    to_group=DEFAULT_GROUP.QA
    cc_group=DEFAULT_GROUP.OP

    if submit and submit["status"] is RELEASE.FAIL:
        return

    if submit and submit["status"] is RELEASE.PASS:
        if submit["type"] in RELEASE.FLOW_QA:
            to_group=DEFAULT_GROUP.OP
            cc_group=DEFAULT_GROUP.QA

    to=[u.mail for u in Group.get_users(to_group)]
    cc=[u.mail for u in Group.get_users(cc_group)]

    sub=u"发布申请:%s"%r.project
    if approvals:
        sub=u"发布确认:%s %s"%(r.project,submit["type"])
        user=User.get(r.apply_uid)
        cc.append(user["mail"])

    try:
        copy_to=User.get(r.copy_to_uid)
        if copy_to:
            cc.append(copy_to["mail"])
    except:pass


    #Referer: http://dev.ops.chinascope.net/templates/release/history.html

    regx=re.compile(r"^http://([a-z.]+)/")

    url="http://%s/templates/release/release.html"%regx.findall(request.headers["Referer"])[0]

    html=render_template(
        "mail.tpl.html",
        sub=sub,
        release=r,
        url=url)

    mail.send(sub,html,to,cc)