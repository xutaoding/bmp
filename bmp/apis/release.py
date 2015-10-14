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

'''
    模块：发布申请
    子模块：申请发布
    权限定义：
    1.任何组都有申请发布权限。
    2.任何组方可查看当前发布进展状况。
    3.QA内部测试，只允许QA进行编辑确认。
    4.运维发布，只允许运维进行编辑确认。
    5.QA外部测试，只允许QA进行编辑确认。
    6.确认人在邮件和其他部门看到的信息中明确标示。
    7.终止需记录到数据库中，附带说明。
    邮件发送规则：
    申请人提交申请后，QA收到邮件进行查看审批，抄送运维，抄送人查看。
    QA确认审批后，运维收到邮件进行查看审批，抄送QA，申请人，抄送人查看。
    运维确认审批后，QA再次收到邮件进行查看审批，抄送运维，申请人，抄送人查看。

    组定义：
    运维：ryan.wang,jim.zhao
    QA:kiki.zhang
    GUEST:其他人
    组是自定义的，在平台中归属组。
'''
class ReleaseApi(BaseApi):
    route=["/release","/release/<int:id>"]
    def auth(self):
        return True

    def get(self,id=None):
        return self.succ(Release.select(id))

    def put(self,id):
        submit=self.request()
        if ReleaseApproval.edit(id,submit):
            return self.succ()

    def post(self):
        submit=self.request()
        Release.add(submit)
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
