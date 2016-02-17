# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.release import Release

from bmp.tasks.release import deploy_database
from bmp import app
from datetime import datetime


class Release_deployApi(BaseApi):
    route = ["/release/deploy/<int:rid>", "/release/deploy/<int:page>/<int:pre_page>"]

    def get(self, page, pre_page):
        return self.succ(Release.undeployed(page, pre_page))

    def post(self, rid):
        result=deploy_database(rid)
        return self.succ(result)

    def put(self, rid):
        Release.deploy(rid)
        return self.succ()


if __name__ == "__main__":
    for i in Release.undeployed(1,100)["items"]:
        print(i["service"]["name"])



