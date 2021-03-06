# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.project import ProjectNotice
from bmp.tasks.mail.project.project_notice import Mail


class Project_noticeApi(BaseApi):
    route = ["/project/notice/<int:page>/<int:pre_page>", "/project/notice"]

    def get(self, page=0, pre_page=None):
        notices = ProjectNotice.select(page, pre_page)
        return self.succ(notices)

    def post(self):
        submit = self.request()
        notice = ProjectNotice.add(submit)

        if submit.__contains__("send_mail") \
                and submit["send_mail"]:
            Mail().to(notice)
        return self.succ()


if __name__ == "__main__":
    pass
