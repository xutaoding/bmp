# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.release import Release


class Release_applyApi(BaseApi):
    route = ["/release/apply/<int:rid>", "/release/apply/<int:page>/<int:pre_page>"]

    def get(self, page=0, pre_page=None):
        return self.succ(Release.drafts(page, pre_page))

    def put(self, rid):
        submit = {"id": rid, "is_draft": False}
        Release.edit(submit)
        return self.succ()


if __name__ == "__main__":
    pass
