# coding=utf-8

import json

from bmp import db
from bmp.models.base import BaseModel
from bmp.models.user import User


# 操作人 权限类型 创建时间 详情（详情里列出每种类型中选择的字段，除了密码字段）
class AccessDeployHistory(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    create_time = db.Column(db.DateTime)
    type = db.Column(db.String(128))
    detail = db.Column(db.Text)

    def _to_dict(self):
        hist = self.to_dict()
        hist["detail"] = json.loads(hist["detail"])
        return hist


class Access(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128))
    status = db.Column(db.String(128))
    content = db.Column(db.Text)

    copy_to_uid = db.Column(db.Text, default="")

    approval_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    approval_time = db.Column(db.DateTime)
    approval_reson = db.Column(db.String(256))

    apply_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    dept = db.Column(db.String(128), default="")
    apply_time = db.Column(db.DateTime)
    apply_reson = db.Column(db.String(256))

    @staticmethod
    def _to_dict(self):
        _dict = self.to_dict()
        _dict["apply_user"] = User.get(_dict["apply_uid"])
        _dict["content"] = json.loads(_dict["content"])
        return _dict
