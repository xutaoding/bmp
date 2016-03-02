# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.leave import Leave
from bmp.models.user import Group
from bmp.const import DEFAULT_GROUP, USER_SESSION
from flask import session


class Leave_searchApi(BaseApi):
    route = ["/leave/search/<string:begin_time>/<string:end_time>",
             "/leave/search/<string:begin_time>/<string:end_time>/<string:name>"]

    def get(self, begin_time, end_time, name="%"):
        if session[USER_SESSION]["uid"] not in Group.get_users(DEFAULT_GROUP.LEAVE.SEARCH):
            name = session[USER_SESSION]["uid"]

        return self.succ(Leave.search(begin_time, end_time, name))


if __name__ == "__main__":
    pass
