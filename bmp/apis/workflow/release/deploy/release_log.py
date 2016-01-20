# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.release import Release

from bmp.tasks.release import deploy_database
from bmp import app


class Release_logApi(BaseApi):
    route = ["/release/deploy/log/<int:rid>"]

    def get(self,rid):
        return self.succ(Release.get_log(rid))

if __name__ == "__main__":
    pass