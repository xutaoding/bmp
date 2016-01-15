# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.release import ReleaseAddress


class Release_deploy_addressApi(BaseApi):
    route = ["/release/deploy/address/<int:aid>",
             "/release/deploy/address",
             "/release/deploy/address/<int:page>/<int:pre_page>"]

    def get(self, page=0, pre_page=None):
        return self.succ(ReleaseAddress.select(page, pre_page))

    def post(self):
        submit = self.request()
        ReleaseAddress.add(submit)
        return self.succ()

    def delete(self,aid):
        ReleaseAddress.delete(aid)
        return self.succ()


if __name__ == "__main__":
    pass
