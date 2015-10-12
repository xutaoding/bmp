#coding: utf-8
from bmp import app
from bmp import db
from bmp.models.user import User
import ldap

def __bind(account,pwd):
    try:
        init=ldap.initialize(app.config["LDAP_HOST"])
        init.simple_bind(account,pwd)
        return init
    except:
        return None


def search(uid="*"):
    init=__bind(app.config["LDAP_ACCOUNT"],app.config["LDAP_PASSWORD"])
    if not init:
        return []

    result=init.search_s(
        app.config["LDAP_BASE_DN"],
        ldap.SCOPE_SUBTREE,
        "(uid=%s)"%(uid),
        [
            "uid",
            "displayName",
            "businessCategory",
            "mail",
            "mobile",
            "title"
        ]
    )
    return result


def auth(uid,pwd):
    result=search(uid)
    if not result:
        return False,None

    dn,user=result[0]
    if not __bind(dn,pwd):
        return False,None
    return True,user


'''
主机：192.168.250.2
端口：389
账号：cn=admin,dc=chinascopefinancial,dc=com
密码：nfUa5gCxXzUNs9ybM8ko
base DN :dc=chinascopefinancial,dc=com
'''

if __name__=="__main__":
   for dn,u in  search("*"):
       print(u)


