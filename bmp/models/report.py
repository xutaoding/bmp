# coding:utf8
from bmp import db
from bmp.models.base import BaseModel


class ReportIssue(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issue = db.Column(db.String(256))
    checked = db.Column(db.Boolean)
    report_id = db.Column(db.Integer, db.ForeignKey("report.id"))


class ReportEditor(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    editor_uid = db.Column(db.String(128),db.ForeignKey("user.uid"))
    team_id = db.Column(db.Integer, db.ForeignKey("report_team.id"))


class ReportTeam(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    is_del = db.Column(db.Boolean, default=False)
    create_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    editors = db.relationship("ReportEditor")

    @staticmethod
    def _to_dict(self):
        _dict=self.to_dict()
        _dict["editors"] = [ReportEditor._to_dict(editor) for editor in self.editors]
        return _dict


class Report(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer, default=0)
    prog = db.Column(db.Integer, default=0)
    schedule = db.Column(db.Text)
    schedule_next = db.Column(db.Text)
    issues = db.relationship("ReportIssue")
    team_id = db.Column(db.Integer, db.ForeignKey("report_team.id"))
    create_time = db.Column(db.DateTime)
    feedback = db.Column(db.String(256))

    @staticmethod
    def _to_dict(self):
        _dict = self.to_dict()
        _dict["issues"] = [ReportIssue._to_dict(issue) for issue in self.issues]
        return _dict
