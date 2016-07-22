# coding=utf-8
import json

from bmp import db
from bmp.apis.base import BaseApi
from bmp.const import ACCESS
from bmp.models.access import Access
from bmp.tasks.access import DeploySsh


class Access_deploy_sshApi(BaseApi):
    route = ["/access/deploy/ssh/<int:aid>"]

    def put(self, aid):
        access = Access.get(aid)
        content = json.loads(access["content"])

        access["status"] = ACCESS.DEPLOY
        Access.edit(access, auto_commit=False)

        deploy = DeploySsh()
        if not deploy.add(content):
            return self.fail()

        db.session.commit()
        return self.succ()
