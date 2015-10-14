#coding: utf-8
from bmp import db
from datetime import datetime
from flask import session
from bmp.const import USER_SESSION

'''
项目名称
发布时间
服务
类型
数据库
表名
从
抄送人
内容

申请人
申请时间
'''

class ReleaseService(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(128),nullable=False)
    type=db.Column(db.String(128),nullable=False)
    database=db.Column(db.String(128))
    table=db.Column(db.String(128))
    release_id=db.Column(db.Integer,db.ForeignKey("release.id"))
    def __init__(self,_dict):
        self.name=_dict["name"]
        self.type=_dict["type"]
        self.database=_dict["database"]
        self.table=_dict["table"]


class ReleaseApproval(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    type=db.Column(db.String(128),unique=True)
    uid=db.Column(db.String(128),nullable=False)
    status=db.Column(db.String(128),nullable=False)
    reson=db.Column(db.String(128))
    options=db.Column(db.String(128))
    release_id=db.Column(db.Integer,db.ForeignKey("release.id"))

    def __init__(self,_dict):
        self.type=_dict["type"]
        self.status=_dict["status"]
        self.reson=_dict["reson"]
        self.options=_dict["options"]
        self.uid=_dict["uid"]

    @staticmethod
    def edit(id,submit):
        approvals=ReleaseApproval.query.filter(
            ReleaseApproval.release_id==id,
            ReleaseApproval.type==submit["type"]).all()

        if not approvals:
            _approval=ReleaseApproval(submit)
            _approval.release_id=id
            db.session.add(_approval)
            db.session.commit()
            return True

        _approval=approvals[0]
        _approval.status=submit["status"]
        _approval.reson=submit["reson"]
        _approval.options=submit["options"]
        db.session.commit()
        return True

class Release(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    project=db.Column(db.String(128),nullable=False)
    content=db.Column(db.String(256))
    copy_to_uid=db.Column(db.String(128))
    release_time=db.Column(db.DateTime,nullable=False)
    apply_uid=db.Column(db.String(128),nullable=False)
    apply_group=db.Column(db.String(128),nullable=False)
    apply_time=db.Column(db.DateTime,nullable=False)
    _from=db.Column(db.String(128),nullable=False)
    to=db.Column(db.String(256),nullable=False)
    approvals=db.relationship("ReleaseApproval")
    service=db.relationship("ReleaseService",uselist=False)

    def __init__(self,_dict):
        self.project=_dict["project"]
        self._from=_dict["_from"]
        self.to=_dict["to"]
        self.release_time=datetime.strptime(_dict["release_time"],"%Y-%m-%d %H:%M:%S")
        self.copy_to_uid=_dict["copy_to_uid"]
        self.content=_dict["content"]

    @staticmethod
    def select(id):
        def __to_dict(release):
            _release=release.to_dict()
            _release["approvals"]=[a.to_dict() for a in release.approvals]
            _release["service"]=release.service.to_dict()
            return _release
        if id==None:
            return [__to_dict(release) for release in Release.query.all()]
        return [__to_dict(release) for release in Release.query.filter(Release.id==id).all()]

    @staticmethod
    def add(submit):
        from bmp.models.user import User
        user=User.query.filter(User.uid==session[USER_SESSION]["uid"]).one()

        release=Release(submit)
        service=ReleaseService(submit["service"])
        release.service=service
        release.approvals=[]
        release.apply_uid=user.uid
        release.apply_group=[g.name for g in user.groups]
        release.apply_time=datetime.now()
        db.session.add(release)
        db.session.commit()
        return True

    @staticmethod
    def approval(id,submit):

        approvals=ReleaseApproval.query.filter(
            ReleaseApproval.release_id==id,
            ReleaseApproval.type==submit["type"]).all()

        if not approvals:
            _approval=ReleaseApproval(submit)
            _approval.release_id=id
            db.session.add(_approval)
            db.session.commit()
            return True

        _approval=approvals[0]
        _approval.status=submit["status"]
        _approval.reson=submit["reson"]
        _approval.options=submit["options"]
        db.session.commit()
        return True


if __name__=="__main__":
    db.create_all()
