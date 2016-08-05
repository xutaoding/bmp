# coding: utf-8

from base import BaseMail
from bmp.utils.user_ldap import Ldap
import json
import traceback


class Mail(BaseMail):
    def to(self, access):
        try:
            ldap = Ldap()

            copy_to_uid = access.copy_to_uid.split(",") \
                if access.copy_to_uid \
                else ldap.get_superior(access.apply_uid, inc_1st=True)

            sub = u" %s权限申请 申请人:%s 申请时间:%s" % (
                access.type,
                access.apply_uid,
                access.apply_time.strftime("%Y-%m-%d %H:%M")
            )

            self.send(
                copy_to_uid,
                sub,
                access=access,
                url="/templates/jurisdiction/curr_apply.html",
                tpl="mail.access.tpl.html"
            )

            return True
        except Exception, e:
            traceback.print_exc()
            return False
