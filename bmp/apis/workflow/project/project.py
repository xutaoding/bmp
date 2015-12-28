# coding: utf-8
from flask import session

from bmp.apis.base import BaseApi
from bmp.models.project import Project
from bmp.const import USER_SESSION


class ProjectApi(BaseApi):
    route = ["/project/<int:page>/<int:pre_page>", "/project/<int:pid>", "/project"]

    def get(self, page=0, pre_page=None, pid=0):
        if pid:
            return self.succ(Project.get(pid))
        return self.succ(Project.select(page, pre_page))

    def post(self):
        submit = self.request()
        Project.add(submit)
        return self.succ()

    def put(self, pid):
        submit = self.request()
        submit["id"]=pid
        Project.edit(submit)
        return self.succ()

    def delete(self, pid):
        Project.delete(pid)
        return self.succ()

    def search(self, page=None, pre_page=None):
        submit = self.request()
        return self.succ(Project.search(submit,page,pre_page))


if __name__ == "__main__":
    from bmp.utils.post import test

    test("post",
         "http://127.0.0.1:5000/apis/v1.0/project",
         {
             "name": "项目名称",
             "desc": "项目描述",
             "summarize": "项目小结",
             "begin_time": "1990-01-01",  # 开始时间
             "end_time": "1990-01-02",  # 计划完成时间
             "demand_uid": "chenglong.yan",  # 需求负责人
             "develop_uid": "chenglong.yan",  # 研发负责人
             "test_uid": "chenglong.yan",  # 测试负责人
             "release_uid": "chenglong.yan",  # 发布负责人
             "man_day": "10",  # 人/天
             "resource": "资源预分配"
         }, True)
