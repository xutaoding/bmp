#coding: utf-8
from bmp import app
import ldap

'''
主机：192.168.250.2
端口：389
账号：cn=admin,dc=chinascopefinancial,dc=com
密码：nfUa5gCxXzUNs9ybM8ko
base DN :dc=chinascopefinancial,dc=com
'''


class User:
    def __init__(self,_dict):
            self.uid=_dict["uid"]
            self.userPassword=_dict["userPassword"]
            self.displayName=_dict["displayName"]
            self.mail=_dict["mail"]
            self.mobile=_dict["mobile"]
            self.title=_dict["title"]


def search(name):
    init=ldap.initialize(app.config["LDAP_HOST"])
    init.simple_bind(app.config["LDAP_ACCOUNT"],app.config["LDAP_PASSWORD"])
    result=init.search_s(
        app.config["LDAP_BASE_DN"],
        ldap.SCOPE_SUBTREE,
        "(uid=%s)"%(name),
        [
            "uid",
            "userPassword",
            "displayName",
            "mail",
            "mobile",
            "title"
        ]
    )
    if not len(result):
        return None
    _dir,user=result[0]
    return User(user)


if __name__=="__main__":
    print search("chenglong.yan")
