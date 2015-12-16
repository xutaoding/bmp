# coding=utf-8
from datetime import datetime
import json

from flask import session

from bmp import db
from bmp.const import USER_SESSION, PROJECT
from bmp.database import Database


class ProjectHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fields = db.Column(db.Text)
    modify_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    modify_time = db.Column(db.DateTime)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

    def __init__(self, _dict):
        self.fields = json.dumps(_dict)
        self.project_id = _dict["project_id"]
        self.modify_uid = session[USER_SESSION]["uid"]
        self.modify_time = datetime.now()

    @staticmethod
    def add(pid, action, _dict):
        _dict["action"] = action
        _dict["project_id"] = pid
        ph = ProjectHistory(_dict)
        db.session.add(ph)


class ProjectScheduleMember(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    schedule_id = db.Column(db.Integer, db.ForeignKey("project_schedule.id"))

    def __init__(self, _dict):
        self.uid = _dict["uid"]


class ProjectSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128))
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(128))
    reson = db.Column(db.String(128))
    desc = db.Column(db.String(256))
    members = db.relationship("ProjectScheduleMember", backref=db.backref("schedule"))
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

    def __init__(self, _dict):
        for k, v in _dict.items():
            if k == "members":
                self.members = Database.to_cls(ProjectScheduleMember, _dict["members"])
            elif "time" in k:
                setattr(self, k, datetime.strptime(v, "%Y-%m-%d"))
            else:
                setattr(self, k, v)

    @staticmethod
    def _to_dict(self):
        _dict = self.to_dict()
        _dict["members"] = [m.to_dict() for m in self.members]
        return _dict

    @staticmethod
    def add(_dict):
        db.session.add(ProjectSchedule(_dict))
        db.session.commit()
        return True

    @staticmethod
    def edit(_dict):
        ps = Database.to_cls(ProjectSchedule, _dict)
        ProjectHistory.add(ps.project_id, PROJECT.EDIT_SCHEDULE(ps.type), _dict)
        db.session.commit()
        return True

    @staticmethod
    @db.transaction
    def edit_members(_dict):
        ps = ProjectSchedule.query.filter(ProjectSchedule.id == _dict["schedule_id"]).one()
        ps.members = [Database.to_cls(ProjectScheduleMember, m) for m in _dict["members"]]
        ProjectHistory.add(ps.project_id, PROJECT.EDIT_MEMBER(ps.type), _dict["members"])
        db.session.flush()


class ProjectDoc(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1024))
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

    def __init__(self, _dict):
        self.url = _dict["url"]


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
    schedules = db.relationship("ProjectSchedule", backref=db.backref("project"))
    historys = db.relationship("ProjectHistory", backref=db.backref("project"))

    def __init__(self, _dict):
        for k, v in _dict.items():
            if "time" in k:
                setattr(self, k, datetime.strptime(v, "%Y-%m-%d"))
            else:
                setattr(self, k, v)

    @staticmethod
    @db.transaction
    def edit(_dict):
        proj = Database.to_cls(Project, _dict)
        ProjectHistory.add(proj.id, PROJECT.EDIT_PROJ, _dict)
        db.session.flush()
        return True

    @staticmethod
    @db.transaction
    def edit_doc(_dict):
        ps = Project.query.filter(Project.id == _dict["project_id"]).one()
        ps.docs = [Database.to_cls(ProjectDoc, d) for d in _dict["docs"]]
        ProjectHistory.add(ps.id, PROJECT.EDIT_DOC, _dict["docs"])
        db.session.flush()

    @staticmethod
    def add(_dict):
        db.session.add(Project(_dict))
        db.session.commit()
        return True

    @staticmethod
    def delete(pid):
        proj = Project.query.filter(Project.id == pid).one()
        db.session.delete(proj)
        db.session.commit()
        return True

    @staticmethod
    def _to_dict(self):
        _dict = self.to_dict()

        _dict["schedules"] = [ProjectSchedule._to_dict(s) for s in self.schedules]
        _dict["historys"] = [h.to_dict() for h in self.historys]
        _dict["docs"] = [d.to_dict() for d in self.docs]
        return _dict

    @staticmethod
    def get(pid):
        return Project._to_dict(Project.query.filter(Project.id == pid).one())

    @staticmethod
    def select(page=0, pre_page=None):
        return Project.query.paginate(page, pre_page, False).to_page(Project._to_dict)
