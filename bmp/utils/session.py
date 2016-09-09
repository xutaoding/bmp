from flask import session

from bmp.const import USER_SESSION
from bmp.models.user import User, Group


def is_admin():
    user = User.query.filter(User.uid == get_uid()).one()
    return user.is_admin


def get_uid():
    return session[USER_SESSION]["uid"]


def in_group(*groups):
    user = User.query.filter(User.uid == get_uid()).one()
    return set([g.name for g in user.groups]).intersection(groups).__len__() > 0


def members(*groups):
    r = []
    for group in groups:
        users = Group.get_users(group)
        r.extend([u.uid for u in users])
    return r

def admins():
    return [u.uid for u in User.query.filter(User.is_admin == True).all()]


if __name__ == "__main__":
    print admins()
