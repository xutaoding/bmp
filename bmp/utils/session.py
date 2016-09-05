from flask import session

from bmp.const import USER_SESSION
from bmp.models.user import User


def is_admin():
    return session[USER_SESSION]["is_admin"]


def get_uid():
    return session[USER_SESSION]["uid"]


def in_group(*groups):
    user = User.query.filter(User.uid == get_uid()).one()
    return set([g.name for g in user.groups]).intersection(groups).__len__() > 0


if __name__ == "__main__":
    pass
