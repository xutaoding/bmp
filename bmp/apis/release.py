#coding: utf-8
from bmp.apis.base import BaseApi
from flask import session
from bmp.const import USER_SESSION
from bmp.utils import user_ldap
from bmp.models.release import Release,ReleaseService,ReleaseApproval
from bmp import db
from bmp.models.user import User
import json
from datetime import datetime
from flask import request
import traceback
import time
from bmp.const import REFS

class ReleaseApi(BaseApi):
    route="/release"
    def auth(self):
        return True

    def get(self):
        return self.succ([r.to_dict() for r in db.session.query(Release).all()])

    def put(self):

        return self.succ()

    def post(self):
        try:
            arg,data=request.form.popitme()
            _submit=json.loads(data)
            release=Release(_submit)

            service=ReleaseService(_submit["service"])
            release.service=service
            release.approvals=[ReleaseApproval(appr) for appr in REFS["审批"]]
            user=User(session[USER_SESSION])
            release.apply_uid=user.uid
            release.apply_time=datetime.now()
            db.session.add(release)
            db.session.commit()
            return self.succ()
        except:
            traceback.print_exc()
            return self.fail()



'''
post={
    "project":"项目名称",
    "service":
        {
            "name":"服务",
            "type":"类型",
            "database":"数据库",
            "table":"表名"
        },
    "_from":"从",
    "to":"到",
    "release_time":"发布时间",
    "copy_to_uid":"抄送人",
    "content":"更改内容"
}
'''
if __name__=="__main__":
    relase=Release.query.all()[0]

    import urllib2,urllib

    data=json.dumps({
        "project":"项目名称",
        "service":
            {
                "name":"服务",
                "type":"类型",
                "database":"数据库",
                "table":"表名"
            },
        "_from":"从",
        "to":"到",
        "release_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "copy_to_uid":"抄送人",
        "content":"更改内容"
    })
    data=urllib.urlencode({"submit":data})
    req=urllib2.Request("http://192.168.0.143:5000/apis/v1.0/release",data)
    rsp=urllib2.urlopen(req)
    print(rsp.read())