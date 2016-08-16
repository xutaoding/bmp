# coding: utf-8

from base import BaseMail
from bmp.utils.user_ldap import Ldap
import json
import traceback
# coding: utf-8

from bmp.models.user import Group, User
from bmp.const import DEFAULT_GROUP
from bmp.tasks.mail.base import BaseMail


class Mail(BaseMail):
    def to(self, access):
        try:
            ldap = Ldap()

            copy_to_uid = [User.get(uid)["mail"] for uid in access.copy_to_uid.split(",")] \
                if access.copy_to_uid \
                else ldap.get_superior(access.apply_uid, inc_1st=True)

            copy_to_uid.extend([u.mail for u in Group.get_users(DEFAULT_GROUP.OP)])


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
