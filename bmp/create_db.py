# coding: utf-8


#todo 自动import modules目录下表定义

from bmp import db
from models.ref import Ref
from const import REFS, DEFAULT_GROUP
from models.user import user_group, Group, User
from models.release import Release, ReleaseApproval, ReleaseService,ReleaseDatabase,ReleaseTable
from models.purchase import Purchase, PurchaseImg, PurchaseGoods, PurchaseApproval, purchase_supplier, \
    purchase_goods_category,purchase_goods_spec
from models.asset import Supplier, Contract, Stock, StockOpt, stock_category,Category,stock_spec_category
from bmp.utils import user_ldap

'''
默认用户组定义：
Guest，默认所有人不需要定义。
QA，KIKI.zhang,aurora.yang,helen.yang
OP（运维），ryan.wang,jim.zhao
'''


def create_all():
    db.create_all()

    u = lambda s: s

    # 导入字典
    for type, names in REFS.items():
        for name in names:
            Ref.add(u(name), u(type))

    # 导入默认用户组
    for group, uids in DEFAULT_GROUP.GROUPS.items():
        for uid in uids:
            result = user_ldap.search(uid)
            dn, user = user_ldap.__user_dict(result)
            if not User.add(user):
                raise Exception("导入用户 %s 失败" % uid)

        uids = [u(uid) for uid in uids]
        Group.add(u(group))
        Group.join(group, uids)


if __name__ == "__main__":
    create_all()
