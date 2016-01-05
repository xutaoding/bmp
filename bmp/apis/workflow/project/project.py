# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.project import Project
from bmp.tasks.mail.project.project_create import mail_to


class ProjectApi(BaseApi):
    route = ["/project/<int:page>/<int:pre_page>", "/project/<int:pid>", "/project"]

    def get(self, page=0, pre_page=None, pid=0):
        if pid: return self.succ(Project.get(pid))
        return self.succ(Project.select(page, pre_page))

    def post(self):
        submit = self.request()
        proj = Project.add(submit)
        mail_to(proj)
        return self.succ()

    def put(self, pid):
        submit = self.request()
        submit["id"] = pid
        Project.edit(submit)
        return self.succ()

    def delete(self, pid):
        Project.delete(pid)
        return self.succ()

    def search(self, page=None, pre_page=None):
        submit = self.request()
        return self.succ(Project.search(submit, page, pre_page))


if __name__ == "__main__":
    print Project.search({"submit": {"status": "新建"}}, 1, 100)
