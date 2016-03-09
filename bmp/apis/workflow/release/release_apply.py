# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.release import Release
from bmp.tasks.mail.release import Mail


class Release_applyApi(BaseApi):
    route = ["/release/apply/<int:rid>", "/release/apply/<int:page>/<int:pre_page>"]

    def get(self, page=0, pre_page=None):
        return self.succ(Release.drafts(page, pre_page))

    def put(self, rid):
        submit = {"id": rid, "is_draft": False}
        release = Release.edit(submit)
        submit["status"] = ""
        submit["type"] = ""
        service=release.service
        if service:
            submit["type"]=service.type

        Mail().to(release,submit)
        return self.succ()


if __name__ == "__main__":
    release=Release.query.all()[0]
    for ser in release:
        print
    print(release.service.type)