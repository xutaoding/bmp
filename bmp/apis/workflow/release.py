# coding=utf-8
from datetime import datetime
from bmp.apis.base import BaseApi
from bmp.models.release import Release, ReleaseApproval
from bmp.tasks.release import mail_to

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
        申请 to QA cc OP、抄送人
        QA确认 to OP cc QA、抄送人、申请人
        运维确认 to QA cc OP、抄送人、申请人

    组定义：
        OP：ryan.wang,jim.zhao
        QA:kiki.zhang
        GUEST:其他人
        组是自定义的，在平台中归属组。
'''


class ReleaseApi(BaseApi):
    route = ["/release", "/release/<int:id>"]

    def get(self, id=0):
        return self.succ(Release.select(id))

    def put(self, id):
        submit = self.request()
        if ReleaseApproval.edit(id, submit):
            mail_to(Release.get(id), submit)
            return self.succ()
        return self.fail()

    def post(self):
        submit = self.request()
        release = Release.add(submit)
        mail_to(release)
        return self.succ()

if __name__ == "__main__":
    pass