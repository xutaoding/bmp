# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.user import User
from bmp.tasks.mail.entry import Mail
from bmp.utils import crypt
from bmp.utils.user_ldap import Ldap


class EntryApi(BaseApi):
    route = ["/users/entry/<string:uid>"]

    def post(self, uid):
        user = User.get(uid)
        user["pwd"] = crypt.randpass()

        ldap = Ldap()
        ldap.reset_pwd(uid, user["pwd"])

        Mail().to(user)
        return self.succ()
