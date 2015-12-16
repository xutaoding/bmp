# coding: utf-8
from flask import session

from bmp.apis.base import BaseApi
from bmp.models.project import Project
from bmp.const import USER_SESSION


class Project_docApi(BaseApi):
    route = ["/project/doc/<int:pid>"]

    def auth(self):
        session[USER_SESSION] = {"uid": "chenglong.yan"}
        return True

    def put(self, pid):
        submit = self.request()
        submit["project_id"] = pid
        Project.edit_doc(submit)
        return self.succ()


if __name__ == "__main__":
    from bmp.utils.post import test

    test("put",
         "http://127.0.0.1:5000/apis/v1.0/project/doc/1",
         {
             "docs": [  # 相关资料
                        {"url": "资料url1"},
                        {"url": "资料url2"}
                        ]
         }, True)
