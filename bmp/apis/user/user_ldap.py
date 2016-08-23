# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.user import User
from bmp.utils import crypt
from bmp.utils.exception import ExceptionEx
from bmp.utils.user_ldap import Ldap


class User_ldapApi(BaseApi):
    route = ["/users/ldap", "/users/ldap/<string:uid>"]

    def get(self, uid="*"):
        ldap = Ldap()
        if uid not in [u"*", "*", None]:
            dn, user = ldap.search(uid, attrlist="*").first()
            return self.succ([user])

        return self.succ(sorted(
            [user for dn, user in ldap.search(attrlist="*").all()],
            lambda x, y: x["employeeNumber"] > y["employeeNumber"]
        ))

    def to_str_dict(self, submit):
        _submit = dict()
        for name, value in submit.items():
            _submit[str(name)] = str(value)
        return _submit

    def post(self, uid):
        submit = self.request()
        submit["uid"] = uid
        submit["c"] = submit["x-csf-emp-nationality"]
        submit["x-csf-emp-pwdReset"] = "TRUE"
        submit["userPassword"] = "chinascope"

        _submit = self.to_str_dict(submit)

        _submit["objectClass"] = [
            "country",
            "x-csf-EmployeeObject",
            "inetOrgPerson",
            "organizationalPerson",
            "person",
            "top"
        ]

        ldap = Ldap()
        ldap.add(uid, _submit)
        User.update()
        return self.succ()

    def put(self, uid):
        submit = self.request()
        ldap = Ldap()
        ldap.modify(uid, self.to_str_dict(submit))
        User.update()
        return self.succ()

    def delete(self, uid):
        ldap = Ldap()

        if uid in ["*", u"*"]:
            raise ExceptionEx("无效的uid")
        else:
            ldap.delete(uid)

        User.update()
        return self.succ()
