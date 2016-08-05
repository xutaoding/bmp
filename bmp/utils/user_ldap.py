# coding: utf-8
import ldap
from ldap import modlist

from bmp import app
from bmp.utils.exception import ExceptionEx


class Ldap:
    def __init__(self):
        self.account = app.config["LDAP_ACCOUNT"]
        self.password = app.config["LDAP_PASSWORD"]
        self.init = ldap.initialize(app.config["LDAP_HOST"])
        self.init.simple_bind_s(self.account, self.password)
        self.search_result = None

    def __del__(self):
        self.init.unbind_s()

    def auth(self, uid, pwd):
        try:
            dn, user = self.search(uid).first()

            init = ldap.initialize(app.config["LDAP_HOST"])
            init.simple_bind_s(dn, pwd)
            init.unbind_s()
            return True
        except:
            return False

    def all(self):
        return self.to_dict()

    def first(self):
        return self.to_dict()[0]

    def to_dict(self):
        result = []
        for dn, user in self.search_result:
            for k in user:
                user[k] = user[k][0]
            result.append((dn, user))
        return result

    def get_superior(self, uid,inc_1st=False):
        try:
            dn, user = self.search(uid).first()

            if inc_1st:
                return list({
                    user["x-csf-emp-2ndManager"].split(",")[0].split("=")[1].strip(),
                    user["x-csf-emp-1stManager"].split(",")[0].split("=")[1].strip()
                })

            return user["x-csf-emp-2ndManager"].split(",")[0].split("=")[1].strip()
        except:
            return None

    def search(self, value="*", field="uid", attrlist=None):
        attr_lst = ["uid",
                    "displayName",
                    "businessCategory",
                    "mail",
                    "mobile",
                    "title",
                    "x-csf-emp-1stManager",
                    "x-csf-emp-2ndManager",
                    "cn",
                    "x-csf-emp-onboardDate"] if not attrlist else attrlist
        if attrlist == "*":
            attr_lst = None

        self.search_result = self.init.search_s(
            app.config["LDAP_BASE_DN"],
            ldap.SCOPE_SUBTREE,
            "(%s=%s)" % (field, value),
            attr_lst
        )
        return self

    def modify(self, uid, _new, password=None):
        dn, _old = self.search(uid, attrlist=_new.keys()).first()
        if password and not self.auth(uid, password):
            return False
        self.init.modify_s(dn, modlist=modlist.modifyModlist(_old, _new))

        return True

    def delete(self, uid):
        dn, user = self.search(uid).first()
        self.init.delete_s(dn)

        return True

    def add(self, uid, submit):
        dn = "uid=%s,dc=employees,dc=people,dc=chinascopefinancial,dc=com" % uid
        try:
            self.init.add_s(dn, modlist.addModlist(submit))
        except ldap.LDAPError as e:
            raise ExceptionEx(e.message)

    def export(self, cols):
        def to_result_dict(u):
            _dict = {}
            for k in u:
                if k in cols:
                    _dict[k] = u[k]
            return _dict

        for dn, u in self.search().all():
            yield to_result_dict(u)

    def reset_pwd(self, uid, newpass=None, oldpass=None):
        try:
            dn, user = self.search(uid).first()
            self.init.passwd_s(dn, oldpass, newpass)
            return True
        except:
            return False


'''
主机：192.168.250.2
端口：389
账号：cn=admin,dc=chinascopefinancial,dc=com
密码：nfUa5gCxXzUNs9ybM8ko
base DN :dc=chinascopefinancial,dc=com
'''

if __name__ == "__main__":
    _ldap = Ldap()
    print _ldap.get_superior("chenglong.yan",inc_1st=True)