# coding: utf-8
import ldap
from ldap import modlist

from bmp import app


def __bind(account, pwd, is_auth=False):
    try:
        init = ldap.initialize(app.config["LDAP_HOST"])
        if not is_auth:
            init.simple_bind(account, pwd)
        else:
            init.simple_bind_s(account, pwd)
            init.unbind_s()
        return init
    except:
        return None


def all():
    users = {}
    for _user in search():
        dn, user = __user_dict([_user])
        users[user["uid"]] = user
    return users


def search(uid="*"):
    init = __bind(app.config["LDAP_ACCOUNT"], app.config["LDAP_PASSWORD"])
    if not init:
        return []

    result = init.search_s(
        app.config["LDAP_BASE_DN"],
        ldap.SCOPE_SUBTREE,
        "(uid=%s)" % (uid),
        [
            "uid",
            "displayName",
            "businessCategory",
            "mail",
            "mobile",
            "title",
            "x-csf-emp-1stManager",
            "x-csf-emp-2ndManager",  # 审批人
            "cn"
        ]
    )

    init.unbind_s()
    return result


def __user_dict(_lst,use_list=False):
    result=[]
    for dn,user in _lst:
        for k in user:
            user[k] = user[k][0]
        result.append((dn,user))
    if not use_list:
        return result[0]
    return result


def auth(uid, pwd):
    result = search(uid)
    if not result:
        return False, None

    dn, user = __user_dict(result)

    if not __bind(dn, pwd, True):
        return False, None
    return True, user


def get_superior(uid):
    try:
        dn, user = __user_dict(search(uid))
        return user["x-csf-emp-2ndManager"].split(",")[0].split("=")[1].strip()
    except:
        return None


def modify(uid, password, _old, _new):
    dn, u = __user_dict(search(uid))
    conn = __bind(dn, password)
    try:
        conn.modify_s(dn, modlist.modifyModlist(_old, _new))
    finally:
        conn.unbind_s()



def export(cols):
    def to_result_dict(u):
        _dict={}
        for k in u:
            if k in cols:
                _dict[k]=u[k]
        return _dict

    for dn,u in __user_dict(search(),True):
        yield to_result_dict(u)



'''
主机：192.168.250.2
端口：389
账号：cn=admin,dc=chinascopefinancial,dc=com
密码：nfUa5gCxXzUNs9ybM8ko
base DN :dc=chinascopefinancial,dc=com
'''

if __name__ == "__main__":
    print(search("ryan.wang"))