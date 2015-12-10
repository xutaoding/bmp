# coding=utf-8
from bmp import db
from flask import session
from bmp.const import USER_SESSION,SCRAP,STOCK
from datetime import datetime
from bmp.database import Database
from bmp.utils.exception import ExceptionEx
import bmp.utils.time as time
from datetime import datetime
from sqlalchemy import and_
import json

class ProjectHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fields = db.Column(db.Text)
    modify_uid=db.Column(db.String(128), db.ForeignKey("user.uid"))
    modify_time=db.Column(db.DateTime)
    project_id=db.Column(db.Integer, db.ForeignKey("project.id"))

    def __init__(self,proj_id,_dict):
        self.fields=json.dumps(_dict)
        self.project_id=proj_id
        self.modify_uid=session[USER_SESSION]["uid"]
        self.modify_time=datetime.now()

    @staticmethod
    def add(proj_id,_dict):
        ph=ProjectHistory(proj_id,_dict)
        db.session.add(ph)

class ProjectScheduleMember(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    schedule_id=db.Column(db.Integer, db.ForeignKey("project_schedule.id"))

class ProjectSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(128))
    reson  = db.Column(db.String(128))
    desc  = db.Column(db.String(256))
    members = db.relationship("ProjectScheduleMember", backref=db.backref("schedule"))
    project_id=db.Column(db.Integer, db.ForeignKey("project.id"))

class ProjectDoc(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1024))
    project_id=db.Column(db.Integer, db.ForeignKey("project.id"))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    desc = db.Column(db.String(256))
    summarize = db.Column(db.Text)
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    demand_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    develop_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    test_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    release_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    man_day = db.Column(db.Integer)
    resource = db.Column(db.String(128))

    docs = db.relationship("ProjectDoc", backref=db.backref("project"))
    schedules = db.relationship("ProjectScheduleMember", backref=db.backref("project"))
    historys = db.relationship("ProjectHistory", backref=db.backref("project"))

    def __init__(self,_dict):
        for k, v in _dict.items():
            if "time" in k:
                setattr(self, k, datetime.strptime(v, "%Y-%m-%d"))
            else:
                setattr(self, k, v)

    @staticmethod
    @db.transaction
    def edit(pid,_dict):
        proj=Project.query.filter(Project.id==pid).one()
        ProjectHistory.add(pid,_dict)

        _dict["id"]=pid
        proj=Database.to_cls(proj,_dict)

        db.session.flush()
        return True

    @staticmethod
    def add(_dict):
        db.session.add(Project(_dict))
        db.session.commit()
        return True

    @staticmethod
    def delete(pid):
        proj=Project.query.filter(Project.id==pid).one()
        db.session.delete(proj)
        db.session.commit()
        return True

    @staticmethod
    def _to_dict(self):
        _dict=self.to_dict()

        def _relation_to_dict(obj,func=None):
            if not obj:
                return ""
            if not func:
                return obj.to_dict()
            return func(obj)

        _dict["schedules"]=_relation_to_dict(self.schedules)
        _dict["historys"]=_relation_to_dict(self.historys)
        _dict["docs"]=_relation_to_dict(self.docs)

    @staticmethod
    def select():
        return [Project._to_dict(p) for p in Project.query.all()]