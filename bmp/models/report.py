# coding:utf8
from bmp import db
from bmp.models.base import BaseModel
from sqlalchemy.orm import validates
from datetime import datetime
from datetime import timedelta
from bmp.utils.exception import ExceptionEx


class ReportIssue(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issue = db.Column(db.String(256))
    checked = db.Column(db.Boolean)
    report_id = db.Column(db.Integer, db.ForeignKey("report.id"))


class ReportTeam(BaseModel,db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    is_del = db.Column(db.Boolean,default=False)


class Report(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer,default=0)
    schedule = db.Column(db.Text)
    schedule_next = db.Column(db.Text)
    issues = db.relationship("ReportIssue")
    team_id = db.Column(db.Integer,db.ForeignKey("report_team.id"))
    create_time = db.Column(db.DateTime)

    @validates("create_time")
    def validate_create_time(self, key, create_time):
        beg_time=(create_time-timedelta(days=create_time.weekday())).replace(hour=0,minute=0,second=0)
        end_time = (create_time + timedelta(days=6 - create_time.weekday())).replace(hour=23, minute=59, second=59)

        if Report.query.filter(Report.create_time.between(beg_time,end_time)).count():
            raise ExceptionEx("本周计划已添加")

        return create_time



    @staticmethod
    def _to_dict(self):
        _dict=self.to_dict()
        _dict["issues"]=[ReportIssue._to_dict(issue) for issue in self.issues]
        return _dict