# coding=utf-8
from datetime import datetime
import json

from flask import session

from bmp import db
from bmp.const import USER_SESSION, PROJECT
from bmp.database import Database
from bmp.utils.exception import ExceptionEx


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

    begin_time_create = db.Column(db.DateTime)
    end_time_create = db.Column(db.DateTime)

    status = db.Column(db.String(128))
    reson = db.Column(db.String(128))
    desc = db.Column(db.String(256))
    members = db.relationship("ProjectScheduleMember", backref=db.backref("schedule"))
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

    def __init__(self, _dict):
        for k, v in _dict.items():
            if k == "members":
                self.members = [Database.to_cls(ProjectScheduleMember, m) for m in _dict["members"]]
            elif "time" in k:
                setattr(self, k, datetime.strptime(v, "%Y-%m-%d"))
            else:
                setattr(self, k, v)

    @staticmethod
    def _to_dict(self):
        _dict = self.to_dict()
        _dict["members"] = [m.to_dict() for m in self.members]
        _dict["status"] = Project._schedule_status(self.end_time_create, self.end_time)
        return _dict

    @staticmethod
    def add(_dict):

        if ProjectSchedule.query \
                .filter(ProjectSchedule.type == _dict["type"]) \
                .filter(ProjectSchedule.project_id == _dict["project_id"]).count():
            raise ExceptionEx("该阶段已添加")

        _dict["begin_time_create"] = _dict["begin_time"]
        _dict["end_time_create"] = _dict["end_time"]

        schedule = ProjectSchedule(_dict)
        db.session.add(schedule)
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
        ProjectHistory.add(ps.project_id, PROJECT.EDIT_MEMBER(ps.type), _dict)
        db.session.flush()


class ProjectDoc(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1024))
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

    def __init__(self, _dict):
        self.url = _dict["url"]
        if _dict.__contains__("project_id"):
            self.project_id = _dict["project_id"]

    @staticmethod
    def add(submit):
        db.session.add(ProjectDoc(submit))
        db.session.commit()

    @staticmethod
    def delete(pid):
        doc = ProjectDoc.query.filter(ProjectDoc.id == pid).one()
        db.session.delete(doc)
        db.session.commit()


class ProjectNotice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128))
    txt = db.Column(db.Text)
    uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    time = db.Column(db.DateTime)

    def __init__(self, _dict):
        for k, v in _dict.items():
            setattr(self, k, v)

        self.uid = session[USER_SESSION]["uid"]
        self.time = datetime.now()

    @staticmethod
    def add(_dict):
        db.session.add(ProjectNotice(_dict))
        db.session.commit()
        return True

    @staticmethod
    def _to_dict(self):
        return self.to_dict()

    @staticmethod
    def select(page=0, pre_page=None):
        return ProjectNotice.query.paginate(page, pre_page, False).order_by(ProjectNotice.time.asc()).to_page(
            ProjectNotice._to_dict)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    desc = db.Column(db.String(256))
    tag = db.Column(db.String(256))
    summarize = db.Column(db.Text)
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    demand_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    develop_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    test_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    release_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    create_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
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
        self.create_uid = session[USER_SESSION]["uid"]

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
        ProjectHistory.add(ps.id, PROJECT.EDIT_DOC, _dict)
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
    def _schedule_status(src_time, dst_time):
        status = PROJECT.STATUS_NEW
        if not (src_time and dst_time):
            return status
        if src_time == dst_time:
            status = PROJECT.STATUS_ON_TIME
        elif src_time > dst_time:
            status = PROJECT.STATUS_AHEAD
        else:
            status = PROJECT.STATUS_DELAY
        return status

    @staticmethod
    def _to_dict(self):
        _dict = self.to_dict()
        _dict["schedules"] = [ProjectSchedule._to_dict(s) for s in self.schedules]
        _dict["historys"] = [h.to_dict() for h in self.historys]
        _dict["docs"] = [d.to_dict() for d in self.docs]

        _dict["status"] = PROJECT.STATUS_NEW
        for sche in _dict["schedules"]:
            if sche["type"] == "release":
                _dict["status"] = Project._schedule_status(_dict["end_time"], sche["end_time"])
        return _dict

    @staticmethod
    def get(pid):
        return Project._to_dict(Project.query.filter(Project.id == pid).one())

    @staticmethod
    def select(page=0, pre_page=None):
        return Project.query.paginate(page, pre_page, False).to_page(Project._to_dict)

    @staticmethod
    def search(submit, page, pre_page):
        def check(s):
            if submit.__contains__(s):
                return submit[s]
            return False

        query = Project.query

        if check("name"):
            query = query.filter(Project.name == check("name"))

        if check("status") and check("status") != PROJECT.STATUS_NEW:
            query = query.join(ProjectSchedule).filter(ProjectSchedule.type == "release")
            if check("status") == PROJECT.STATUS_ON_TIME:
                query = query.filter(Project.end_time == ProjectSchedule.end_time)
            elif check("status") == PROJECT.STATUS_AHEAD:
                query = query.filter(Project.end_time > ProjectSchedule.end_time)
            else:
                query = query.filter(Project.end_time < ProjectSchedule.end_time)
        else:
            query = query.filter(~Project.id.in_([ps.id for ps in ProjectSchedule.query.all()]))

        return query.paginate(page, pre_page, False).to_page(Project._to_dict)
