# coding: utf-8
from bmp import db
from datetime import datetime
from flask import session
from bmp.const import USER_SESSION
from bmp.const import DEFAULT_GROUP
from bmp.utils.exception import ExceptionEx

class ReleaseTable(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    release_database_id=db.Column(db.Integer,db.ForeignKey("release_database.id"))
    def __init__(self,_dict):
        self.name=_dict["name"]


class ReleaseDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    tables = db.relationship("ReleaseTable")
    release_service_id=db.Column(db.Integer,db.ForeignKey("release_service.id"))

    @staticmethod
    def _to_dict(self):
        database=self.to_dict()
        database["tables"]=[t.to_dict() for t in self.tables]
        return database

    def __init__(self,_dict):
        self.name=_dict["name"]
        self.tables = [ReleaseTable(t) for t in _dict["table"]]

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
        service=self.to_dict()
        service["databases"] = [ReleaseDatabase._to_dict(d) for d in self.databases]
        return service

    def __init__(self, _dict):
        self.name = _dict["name"]
        self.type = _dict["type"]
        #self.database = _dict["database"]
        #self.table = _dict["table"]
        databases=[d for d in _dict["database"].split("|") if d!=""]
        tables=[t for t in _dict["table"].split("|") if t!=""]
        if len(databases)!=len(tables):
            raise ExceptionEx("表格式错误")

        def format_database(database,table):
            _database={"name":database.strip()}
            def format_tables(table):
                return [{"name":t.strip()} for t in table.split(",")]
            _database["table"]=[t for t in format_tables(table)]
            return _database

        _dict["database"]=[format_database(databases[i],tables[i]) for i in range(0,len(databases))]

        self.databases = [ReleaseDatabase(t) for t in _dict["database"]]


class ReleaseApproval(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128))
    uid = db.Column(db.String(128), db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(128), nullable=False)
    reson = db.Column(db.String(128))
    options = db.Column(db.String(128))
    release_id = db.Column(db.Integer, db.ForeignKey("release.id"))

    def __init__(self, _dict=None):
        self.type = _dict["type"]
        self.status = _dict["status"]
        self.reson = _dict["reson"]
        self.options = _dict["options"]
        self.uid = _dict["uid"]

    @staticmethod
    @db.transaction
    def edit(id, submit):
        approval = ReleaseApproval.query.filter(
            ReleaseApproval.release_id == id,
            ReleaseApproval.type == submit["type"])

        if not approval.count():
            _approval = ReleaseApproval(submit)
            _approval.release_id = id
            db.session.add(_approval)
            db.session.flush()
            return True

        _approval = approval.one()
        _approval.status = submit["status"]
        _approval.reson = submit["reson"]
        _approval.options = submit["options"]
        db.session.flush()
        return True

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

    def __init__(self, _dict):
        self.project = _dict["project"]
        self._from = _dict["_from"]
        self.to = _dict["to"]
        self.release_time = datetime.strptime(_dict["release_time"], "%Y-%m-%d %H:%M")
        self.copy_to_uid = _dict["copy_to_uid"]
        self.content = _dict["content"]

    @staticmethod
    def select(id=0, uid=0):
        def __to_dict(release):
            _release = release.to_dict()
            _release["approvals"] = [a.to_dict() for a in release.approvals]
            _release["service"] = ReleaseService._to_dict(release.service)
            return _release

        query = Release.query.order_by(Release.apply_time.desc())

        if not id:
            if not uid:
                return [__to_dict(release) for release in query.all()]
            return [__to_dict(release) for release in query.filter(Release.apply_uid == uid).all()]
        return [__to_dict(release) for release in query.filter(Release.id == id).all()]

    @staticmethod
    def get(rid):
        return Release.query.filter(Release.id == rid).one()

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

if __name__ == "__main__":
    for service in ReleaseService.query.all():
        databases=service.database.split("|")
        tables=service.table.split("|")
        if len(databases)!=len(tables):
            print(databases,tables)
            continue
        def format_database(database,table):
            _database={"name":database.strip()}
            def format_tables(table):
                return [{"name":t.strip()} for t in table.split(",")]
            _database["table"]=[t for t in format_tables(table)]
            return _database
        _databases=[ReleaseDatabase(format_database(databases[i],tables[i])) for i in range(0,len(databases))]
        service.databases=_databases






