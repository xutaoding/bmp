#coding=utf-8

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
    route=["/release","/release/<int:id>"]
    def auth(self):
        return True

    def get(self,id=None):
        def __to_dict(release):
            _release=release.to_dict()
            _release["approvals"]=[a.to_dict() for a in release.approvals]
            _release["service"]=release.service.to_dict()
            return _release
        if id!=None:
            self.succ([__to_dict(release) for release in Release.query.all()])
        return self.succ([__to_dict(release) for release in Release.query.filter(Release.id==id).all()])

    def put(self,id):
        approval=self.request()
        approvals=ReleaseApproval.query.filter(
            ReleaseApproval.release_id==id,
            ReleaseApproval.type==approval["type"]).all()

        if not approvals:
            _approval=ReleaseApproval(approval)
            _approval.release_id=id
            db.session.add(_approval)
            db.session.commit()
            return self.succ()

        _approval=approvals[0]
        _approval.status=approval["status"]
        _approval.reson=approval["reson"]
        _approval.options=approval["options"]
        db.session.commit()
        return self.succ()

    def post(self):
        submit=self.request()
        release=Release(submit)
        service=ReleaseService(submit["service"])
        release.service=service
        release.approvals=[]
        release.apply_uid=User(session[USER_SESSION]).uid
        release.apply_time=datetime.now()
        db.session.add(release)
        db.session.commit()
        return self.succ()

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

    from bmp.utils.post import test

    test(
        "put",
        "http://192.168.0.143:5000/apis/v1.0/release/2",
        {
            "type":"QA内部测试",
            "uid":"审批人",
            "status":"审批状态",
            "reson":"退回理由!",
            "options":"BUG,文件未成功修改,发布问题"
        }
    )

    test(
        "post",
        "http://192.168.0.143:5000/apis/v1.0/release",
        {
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
        },True
    )
