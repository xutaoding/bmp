# coding: utf-8
from bmp.models.user import Group, User
from flask import render_template
import bmp.utils.mail as mail
from flask import request
import re
from bmp.const import RELEASE, DEFAULT_GROUP
import traceback
from bmp import log


def mail_to(r, submit=None):
    try:
        __mail_to(r, submit)
    except Exception, e:
        traceback.print_exc()
        log.exception(e)


def __mail_to(r, submit):
    approvals = r.approvals
    to, cc = [], []
    to_group = [DEFAULT_GROUP.QA]
    to_group.extend([DEFAULT_GROUP.OP])
    for g in to_group:
        to.extend([u.mail for u in Group.get_users(g)])

    user = User.get(r.apply_uid)
    sub = u"发布申请:%s" % r.project
    if submit and submit["status"] == RELEASE.FAIL:
        sub = u"发布退回:%s %s" % (r.project, submit["type"])
        to = [user["mail"]]
    elif approvals:
        sub = u"发布确认:%s %s" % (r.project, submit["type"])
        to.append(user["mail"])

    try:
        copy_to = User.get(r.copy_to_uid)
        if copy_to["mail"] not in to:
            cc.append(copy_to["mail"])
    except:
        pass


    # Referer: http://dev.ops.chinascope.net/templates/release/history.html

    regx = re.compile(r"^http://([a-z.]+)/")

    url = ""  # http://%s/templates/release/release.html"%regx.findall(request.headers["Referer"])[0]

    html = render_template(
        "mail.tpl.html",
        sub=sub,
        release=r,
        approvals=approvals,
        url=url)

    mail.send(sub, html, list(set(to)), cc)
