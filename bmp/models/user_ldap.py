#coding: utf-8
from bmp import app
import ldap

FIELDS='''
dn
entryUUID
preferredLanguage
userPassword
mail
displayName
x-csf-emp-1stManager
title
modifyTimestamp
createTimestamp
employeeNumber
uid
entryCSN
modifiersName
sn
entryDN
x-csf-emp-onboardDate
st
creatorsName
structuralObjectClass
c
subschemaSubentry
givenName
mobile
objectClass
cn
l
hasSubordinates
x-csf-emp-nationality
employeeType
businessCategory
x-csf-emp-grade
x-csf-emp-pwdReset
x-csf-emp-gender
"""
"""
主机：192.168.250.2
端口：389
账号：cn=admin,dc=chinascopefinancial,dc=com
密码：nfUa5gCxXzUNs9ybM8ko
base DN :dc=chinascopefinancial,dc=com
'''


class User:
    def __init__(self,_dict):
        self.cn=_dict["cn"]
        self.displayName=_dict["displayName"]
        self.employeeNumber=_dict["employeeNumber"]
        self.employeeType=_dict["employeeType"]
        self.givenName=_dict["givenName"]
        self.l=_dict["l"]

def users():
    init=ldap.initialize(app.config["LDAP_HOST"])
    init.simple_bind(app.config["LDAP_ACCOUNT"],app.config["LDAP_PASSWORD"])
    users=init.search_s(
        app.config["LDAP_BASE_DN"],
        ldap.SCOPE_SUBTREE,
        "(objectClass=*)",["cn"])

if __name__=="__main__":
    init=ldap.initialize("ldap://192.168.250.2")
    init.simple_bind("cn=admin,dc=chinascopefinancial,dc=com","nfUa5gCxXzUNs9ybM8ko")
    users=init.search_s(
        "dc=chinascopefinancial,dc=com",
        ldap.SCOPE_SUBTREE,
        "(objectClass=*)",
        [
            "cn",
            "displayName",
            "employeeNumber",
            "employeeType",
            "givenName"
        ])
    for user in users:
        print(user)