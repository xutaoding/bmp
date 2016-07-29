# coding=utf-8

import json
from datetime import datetime

from bmp import db
from bmp.apis.base import BaseApi
from bmp.apis.workflow.access.deploy.access_deploy_history import AccessDeployHistory
from bmp.const import USER_SESSION
from bmp.tasks.access import DeploySsh
from bmp.utils.exception import ExceptionEx
from flask import session


class Access_deploy_sshApi(BaseApi):
    route = ["/access/deploy/ssh"]

    def post(self):
        submit = self.request()
        typ = submit.pop("type")
        detail = json.dumps(submit)

        ssh = DeploySsh()

        AccessDeployHistory.add(
            {
                "create_uid": session[USER_SESSION]["uid"],
                "create_time": datetime.now(),
                "type": typ,
                "detail": detail
            }, auto_commit=False)

        ret = ssh.add(submit)

        if "ok" not in ret:
            raise ExceptionEx("添加失败" % ret)

        db.session.commit()
        return self.succ()


if __name__ == "__main__":
    ssh = DeploySsh(timeout=None)
    print ssh.add({"user_name": "chenglong.yan", "hosts": ["192.168.250.111"], "gen_key": "1", "role": "root"})

