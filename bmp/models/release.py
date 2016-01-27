# coding: utf-8
from datetime import datetime

from flask import session

from bmp import db
from bmp.const import USER_SESSION
from bmp.const import DEFAULT_GROUP
from bmp.utils.exception import ExceptionEx
from bmp.const import RELEASE,RELEASE_SERVICE
from bmp.database import Database

class ReleaseLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    release_id = db.Column(db.Integer,db.ForeignKey("release.id"))

    def __init__(self,content):
        self.content=content["content"]


class ReleaseTable(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    release_database_id = db.Column(db.Integer, db.ForeignKey("release_database.id"))

    def __init__(self, _dict):
        self.name = _dict["name"]


class ReleaseDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    tables = db.relationship("ReleaseTable")
    release_service_id = db.Column(db.Integer, db.ForeignKey("release_service.id"))

    @staticmethod
    def _to_dict(self):
        database = self.to_dict()
        database["tables"] = [t.to_dict() for t in self.tables]
        return database

    def __init__(self, _dict):
        self.name = _dict["name"]
        self.tables = [Database.to_cls(ReleaseTable, t) for t in _dict["table"]]


class ReleaseService(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    database = db.Column(db.String(128))
    table = db.Column(db.String(128))
    databases = db.relationship("ReleaseDatabase")
    release_id = db.Column(db.Integer, db.ForeignKey("release.id"))

    @staticmethod
    def _to_dict(self):
        service = self.to_dict()
        service["databases"] = [ReleaseDatabase._to_dict(d) for d in self.databases]
        return service

    def __init__(self, _dict):
        self.name = _dict["name"]
        self.type = _dict["type"]
        databases = [d for d in _dict["database"].split("|") if d != ""]
        tables = [t for t in _dict["table"].split("|") if t != ""]
        if len(databases) != len(tables):
            raise ExceptionEx("表格式错误")

        def format_database(database, table):
            _database = {"name": database.strip()}

            def format_tables(table):
                return [{"name": t.strip()} for t in table.split(",")]

            _database["table"] = [t for t in format_tables(table)]
            return _database

        _dict["database"] = [format_database(databases[i], tables[i]) for i in range(0, len(databases))]

        self.databases = [Database.to_cls(ReleaseDatabase, t) for t in _dict["database"]]


class ReleaseApproval(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128))
    uid = db.Column(db.String(128), db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(128), nullable=False)
    reson = db.Column(db.String(128))
    desc = db.Column(db.String(128))
    options = db.Column(db.String(128))
    release_id = db.Column(db.Integer, db.ForeignKey("release.id"))

    def __init__(self, _dict=None):
        self.type = _dict["type"]
        self.status = _dict["status"]
        self.reson = _dict["reson"]
        self.desc = _dict["desc"]
        self.options = _dict["options"]
        self.uid = _dict["uid"]

    @staticmethod
    @db.transaction
    def edit(id, submit):
        approval = ReleaseApproval.query.filter(
            ReleaseApproval.release_id == id,
            ReleaseApproval.type == submit["type"])

        if approval.count():
            raise ExceptionEx("%s 已审批" % submit["type"])
        _approval = ReleaseApproval(submit)
        _approval.release_id = id

        release = Release.query.filter(Release.id == id).one()

        if _approval.status == RELEASE.FAIL or len(release.approvals) == 2:
            release.is_finished = True

        db.session.add(_approval)
        db.session.flush()
        return True


class ReleaseAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    addr = db.Column(db.String(256))
    type = db.Column(db.String(128))  # d_host s_host

    def __init__(self, _dict):
        self.name = _dict["name"]
        self.addr = _dict["addr"]
        self.type = _dict["type"]

    @staticmethod
    def add(submit):
        ra = ReleaseAddress(submit)
        db.session.add(ra)
        db.session.flush()
        return True

    @staticmethod
    def delete(aid):
        ra = ReleaseAddress.query.filter(ReleaseAddress.id == aid).one()
        db.session.delete(ra)
        db.session.commit()
        return True

    @staticmethod
    def _to_dict(self):
        return self.to_dict()

    @staticmethod
    def select(page=0, pre_page=None):
        return ReleaseAddress.query.paginate(page, pre_page).to_page(ReleaseAddress._to_dict)


class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(256))
    copy_to_uid = db.Column(db.String(128), db.ForeignKey("user.id"))
    release_time = db.Column(db.DateTime, nullable=False)
    apply_uid = db.Column(db.String(128), db.ForeignKey("user.id"), nullable=False)
    apply_group = db.Column(db.String(128), nullable=False)
    apply_time = db.Column(db.DateTime, nullable=False)
    _from = db.Column(db.String(128), nullable=False)
    to = db.Column(db.String(256), nullable=False)
    approvals = db.relationship("ReleaseApproval")
    service = db.relationship("ReleaseService", uselist=False)
    log = db.relationship("ReleaseLog",uselist=False)
    release_type = db.Column(db.String(64), default="")
    is_finished = db.Column(db.Boolean, default=False)
    is_deployed = db.Column(db.Boolean, default=False)
    is_deploying = db.Column(db.Boolean, default=False)
    deploy_time = db.Column(db.DateTime)
    deploy_times = db.Column(db.Integer,default=0)


    def __init__(self, _dict):
        self.project = _dict["project"]
        self._from = _dict["_from"]
        self.to = _dict["to"]
        self.release_time = datetime.strptime(_dict["release_time"], "%Y-%m-%d %H:%M")
        self.copy_to_uid = _dict["copy_to_uid"]
        self.content = _dict["content"]
        self.release_type = _dict["release_type"]

    @staticmethod
    def _to_dict(release,show_log=False):
        _release = release.to_dict()
        _release["approvals"] = [a.to_dict() for a in release.approvals]
        _release["service"] = ReleaseService._to_dict(release.service)
        if show_log:
            log=release.log
            if log:
                _release["log"]=log.content
            else:
                _release["log"]=""

        return _release

    @staticmethod
    def get_log(rid):
        release=Release.query.filter(Release.id==rid).one()
        log=release.log
        if not log:return ""
        return log.content.replace("\n","\r")

    @staticmethod
    def add_log(rid,log_path):
        with open(log_path) as log:
            __dict={"content":log.read()}
            release=Release.query.filter(Release.id==rid).one()
            query_log=ReleaseLog.query.filter(ReleaseLog.release_id==rid)
            if query_log.count():
                __dict["id"]=query_log.one().id
            release.log=Database.to_cls(ReleaseLog,__dict)
        db.session.commit()
        return True

    @staticmethod
    def select(page, pre_page):
        page = Release.query.order_by(Release.apply_time.desc()).paginate(page, pre_page)
        return page.to_page(Release._to_dict)

    @staticmethod
    def unfinished(page, pre_page):
        page = Release.query \
            .filter(Release.is_finished == False) \
            .order_by(Release.apply_time.desc()) \
            .paginate(page, pre_page)
        return page.to_page(Release._to_dict)

    @staticmethod
    def self(page, pre_page):
        page = Release.query \
            .filter(Release.is_finished == False) \
            .filter(Release.apply_uid == session[USER_SESSION]["uid"]) \
            .order_by(Release.apply_time.desc()) \
            .paginate(page, pre_page)
        return page.to_page(Release._to_dict)

    @staticmethod
    def deployed(page, pre_page):
        page = Release.query \
            .filter(Release.is_deployed == True) \
            .order_by(Release.apply_time.desc()) \
            .paginate(page, pre_page)
        return page.to_page(Release._to_dict)

    @staticmethod
    def undeployed(page, pre_page):
        page = Release.query \
            .join(ReleaseApproval) \
            .join(ReleaseService)\
            .filter(ReleaseService.name==RELEASE_SERVICE.DATA_BASE)\
            .filter(Release.is_finished == False) \
            .filter(ReleaseApproval.type == RELEASE.FLOW_TEST) \
            .filter(ReleaseApproval.status == RELEASE.PASS) \
            .filter(Release.is_deployed == False) \
            .order_by(Release.apply_time.desc()) \
            .paginate(page, pre_page)
        return page.to_page(Release._to_dict)

    @staticmethod
    def finished(page, pre_page):
        page = Release.query \
            .filter(Release.is_finished == True) \
            .order_by(Release.apply_time.desc()) \
            .paginate(page, pre_page)
        return page.to_page(Release._to_dict)

    @staticmethod
    def between(begin, end):
        return [Release._to_dict(release) for release in
                Release.query.filter(Release.apply_time.between(begin, end)).all()]

    @staticmethod
    def get(rid):
        return Release._to_dict(Release.query.filter(Release.id == rid).one())

    @staticmethod
    @db.transaction
    def add(submit):
        from bmp.models.user import User
        user = User.query.filter(User.uid == session[USER_SESSION]["uid"]).one()

        release = Release(submit)
        service = ReleaseService(submit["service"])
        release.service = service
        release.approvals = []
        release.apply_uid = user.uid
        if user.groups:
            release.apply_group = user.groups[0].name
        else:
            release.apply_group = DEFAULT_GROUP.GUEST

        release.apply_time = datetime.now()
        db.session.add(release)
        db.session.flush()
        return release

    @staticmethod
    @db.transaction
    def edit(submit):
        release = Database.to_cls(Release, submit)
        release.service = Database.to_cls(ReleaseService, submit["service"])
        db.session.flush()
        return True

    @staticmethod
    @db.transaction
    def approval(id, submit):

        approvals = ReleaseApproval.query.filter(
            ReleaseApproval.release_id == id,
            ReleaseApproval.type == submit["type"]).all()

        if not approvals:
            _approval = ReleaseApproval(submit)
            _approval.release_id = id
            db.session.add(_approval)
            db.session.commit()
            return True

        _approval = approvals[0]
        _approval.status = submit["status"]
        _approval.reson = submit["reson"]
        _approval.options = submit["options"]
        db.session.commit()
        return True

    @staticmethod
    def deploy(rid):
        release = Release.query.filter(Release.id == rid).one()
        release.is_deployed = True
        db.session.commit()
        return True


if __name__ == "__main__":
    Release.query.filter(Release)
