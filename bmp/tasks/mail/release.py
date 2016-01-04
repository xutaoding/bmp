# coding: utf-8
import re

from flask import render_template
from flask import request

from bmp.models.user import Group, User
import bmp.utils.mail as mail
from bmp.const import RELEASE, DEFAULT_GROUP
import traceback


def mail_to(r, submit):
    try:
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

        host=regx.findall(request.headers["Referer"])[0]

        if "dev" in host:
            sub=u"【测试】 %s"%sub

        url = "http://%s/templates/release/release.html" % host

        html = render_template(
            "mail.tpl.html",
            sub=sub,
            release=r,
            approvals=approvals,
            url=url)

        mail.send(sub, html, list(set(to)), cc)
    except:
        traceback.print_exc()