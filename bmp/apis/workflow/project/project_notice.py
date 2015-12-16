# coding: utf-8
from flask import session

from bmp.apis.base import BaseApi
from bmp.models.project import ProjectNotice
from bmp.const import USER_SESSION


class Project_noticeApi(BaseApi):
    route = ["/project/notice/<int:page>/<int:pre_page>","/project/notice"]

    def auth(self):
        session[USER_SESSION] = {"uid": "chenglong.yan"}
        return True

    def get(self, page=0, pre_page=None):
        notices=ProjectNotice.select(page,pre_page)
        return self.succ(notices)

    def post(self):
        submit = self.request()
        ProjectNotice.add(submit)
        return self.succ()

if __name__ == "__main__":
    from bmp.utils.post import test

    test("post",
         "http://127.0.0.1:5000/apis/v1.0/project/notice",
         {
             "type":"随便聊聊",
             "txt":"testtesttesttesttesttest"
         }, True)
