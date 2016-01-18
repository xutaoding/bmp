# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.project import Project, ProjectDoc


class Project_docApi(BaseApi):
    route = ["/project/doc/<int:pid>"]

    def put(self, pid):
        submit = self.request()
        submit["project_id"] = pid
        Project.edit_doc(submit)
        return self.succ()

    def post(self, pid):
        submit = self.request()
        submit["project_id"] = pid
        ProjectDoc.add(submit)
        return self.succ()

    def delete(self, pid):
        ProjectDoc.delete(pid)
        return self.succ()


if __name__ == "__main__":
    pass
