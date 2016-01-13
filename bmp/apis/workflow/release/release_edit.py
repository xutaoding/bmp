# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.release import Release, ReleaseApproval
from bmp.tasks.mail.release import mail_to


class Release_editApi(BaseApi):
    route = ["/release/edit/<int:rid>"]

    def put(self,rid):
        submit = self.request()
        submit["id"]=rid
        Release.edit(submit)
        return self.succ()

if __name__ == "__main__":
    pass
