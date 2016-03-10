# coding: utf-8
from datetime import datetime

from flask import session

from bmp import db
from bmp.const import USER_SESSION
from bmp.utils.exception import ExceptionEx

user_group = db.Table("user_group",
                      db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                      db.Column("group_id", db.Integer, db.ForeignKey("group.id")))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    desc = db.Column(db.String(128))
    is_buildin = db.Column(db.Boolean, default=False)
    users = db.relationship("User", secondary=user_group, backref=db.backref("groups"))

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    @staticmethod
    def join(name, users):
        group = Group.query.filter(Group.name == name).one()
        if users:
            group.users = User.query.filter(User.uid.in_(users)).all()
        else:
            group.users = []
        db.session.commit()
        return True

    @staticmethod
    def edit(name, new_name, new_desc):
        name, new_name = name.upper(), new_name.upper()
        group = Group.query.filter(Group.name == name).one()
        if name != new_name and group.is_buildin:
            raise ExceptionEx("内建组禁止修改组名")

        group.name = new_name
        group.desc = new_desc
        db.session.commit()
        return True

    @staticmethod
    @db.transaction
    def add(name, desc):
        if Group.query.filter(Group.name == name).count():
            return False
        db.session.add(Group(name, desc))
        db.session.flush()
        return True

    @staticmethod
    @db.transaction
    def delete(name):
        group = Group.query.filter(Group.name == name).one()
        if group.is_buildin:
            raise ExceptionEx("禁止删除内建组")
        db.session.delete(group)
        db.session.flush()
        return True

    @staticmethod
    def get(name):
        return Group.query.filter(Group.name.like(name)).one()

    @staticmethod
    def _to_dict(group):
        g = group.to_dict()
        g["users"] = [u.uid for u in group.users]
        return g

    @staticmethod
    def select(name="%", to_dict=True):
        if to_dict:
            return [Group._to_dict(g) for g in Group.query.filter(Group.name.like(name)).all()]
        return Group.query.filter(Group.name.like(name)).all()

    @staticmethod
    def get_descs():
        descs = {}
        for g in Group.query.all():
            descs[g.name] = g.desc
        return descs

    @staticmethod
    def get_users(name):
        g = Group.get(name)
        return g.users


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128), unique=True, nullable=False)
    displayName = db.Column(db.String(128))
    mail = db.Column(db.String(128))
    mobile = db.Column(db.String(128))
    title = db.Column(db.String(128))
    businessCategory = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    create_time = db.Column(db.DateTime)
    last_time = db.Column(db.DateTime)
    is_dimiss = db.Column(db.Boolean, default=False)

    def __eq__(self, other):
        return self.uid == other.uid

    def __init__(self, _dict):
        for k, item in _dict.items():
            setattr(self, k, item)

    @staticmethod
    def __add_group(user):
        _user = user.to_dict()
        _user["group"] = [g.name for g in user.groups]
        return _user

    @staticmethod
    def uids():
        return [u.uid for u in User.query.all()]

    @staticmethod
    def select(uid="%"):
        query = User.query.order_by(User.uid.asc())
        if uid != "%":
            query = User.query.filter(User.uid == uid).order_by(User.uid.asc())
        user = User.query.filter(User.uid == session[USER_SESSION]["uid"]).one()
        users = query.filter(User.is_dimiss == False).all()
        users.pop(users.index(user))
        users.insert(0, user)
        return [User.__add_group(u) for u in users]

    @staticmethod
    def get(uid):
        user = User.query.filter(User.is_dimiss == False).filter(User.uid == uid).one()
        return User.__add_group(user)

    @staticmethod
    @db.transaction
    def edit(submit):
        user = User.query.filter(User.uid == submit["uid"]).one()
        user.__init__(submit)
        db.session.flush()
        return True

    @staticmethod
    @db.transaction
    def set_groups(uid, groups):
        user = User.query.filter(User.uid == uid).one()
        user.groups = Group.query.filter(Group.name.in_(groups.split(","))).all()
        db.session.flush()
        return True

    @staticmethod
    @db.transaction
    def delete(uid):
        user = User.query.filter(User.uid == uid).one()
        db.session.delete(user)
        db.session.flush()
        return True

    @staticmethod
    @db.transaction
    def add(_dict):
        new_user = User(_dict)
        user = User.query.filter(User.uid == new_user.uid)
        if user.count():
            user = user.one()
            user.last_time = datetime.now()
            db.session.flush()
            return True

        new_user.is_admin = False
        new_user.create_time = datetime.now()
        new_user.last_time = datetime.now()
        db.session.add(new_user)
        db.session.flush()
        return True

    @staticmethod
    @db.transaction
    def update(_ldaps):
        users = User.query.all()
        user_dict = {}
        for user in users:
            user_dict[user.uid] = user

        # 删除离职的
        for uid in set(user_dict.keys()).difference(_ldaps.keys()):
            user_dict[uid].is_dimiss = True

        # 修改存在的
        for uid in set(user_dict.keys()).intersection(_ldaps.keys()):
            u, ldap = user_dict[uid], _ldaps[uid]
            u.is_dimiss = False
            for field in ldap.keys():
                setattr(u, field, ldap[field])

        # 添加新增的
        for uid in set(_ldaps.keys()).difference(user_dict.keys()):
            user = User(_ldaps[uid])
            user.create_time = datetime.now()
            user.last_time = datetime.now()
            user.is_admin = False
            db.session.add(user)

        db.session.flush()
        return True

    @staticmethod
    def get_business_category(bc):
        return User.query.filter(User.is_dimiss == False).filter(User.businessCategory == bc).all()


if __name__ == "__main__":
    pass