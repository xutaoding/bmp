# coding=utf-8
import json
from datetime import datetime

from flask import session

from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION, ACCESS
from bmp.models.access import Access


class AccessApi(BaseApi):
    route = ["/access", "/access/<int:aid>", "/access/<int:page>/<int:pre_page>"]

    # 申请人 申请时间 类型 理由 内容 操作
    def get(self, page=0, pre_page=None, aid=0):
        if aid:
            return self.succ(Access.get(aid))

        return self.succ(Access.select(
            page=page,
            pre_page=pre_page,
            _filters=Access.status == ACCESS.NEW
        ))

    def post(self):
        submit = self.request()
        submit["apply_time"] = datetime.now()
        submit["apply_uid"] = session[USER_SESSION]["uid"]
        submit["content"] = json.dumps(submit["content"])

        Access.add(submit)
        return self.succ()

    def put(self, aid):
        submit = self.request()
        submit["id"] = aid
        submit["content"] = json.dumps(submit["content"])

        Access.edit(submit)
        return self.succ()

    def delete(self, aid):

        Access.delete(aid)
        return self.succ()


if __name__ == "__main__":
    pass
