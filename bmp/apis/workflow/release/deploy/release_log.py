# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.release import Release

from bmp.tasks.release import deploy_database
from bmp import app


class Release_logApi(BaseApi):
    route = ["/release/deploy/log"]

    def get(self):
        return self.succ(filename="%s/data_deploy_log/myapp.log" % app.root_path)

if __name__ == "__main__":
    pass