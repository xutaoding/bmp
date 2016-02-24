# coding=utf-8

from flask import session
from sqlalchemy import or_, and_

from bmp import db
from bmp.database import Database
from bmp.const import USER_SESSION
from bmp.utils.exception import ExceptionEx
from bmp.utils import user_ldap
from bmp.const import LEAVE
from datetime import datetime


class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    reson = db.Column(db.String(128))
    type_id = db.Column(db.Integer, db.ForeignKey("ref.id"))
    dept = db.Column(db.String(128))
    days = db.Column(db.Float)
    tel = db.Column(db.String(128))
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(128), nullable=False)
    feedback = db.Column(db.String(128), nullable=True)

    copy_to_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))

    approval_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    approval_time = db.Column(db.DateTime)

    def __init__(self, _dict):
        for k, v in _dict.items():
            if "time" in k:
                setattr(self, k, datetime.strptime(v, "%Y-%m-%d"))
            else:
                setattr(self, k, v)

        if not _dict.__contains__("id"):
            self.uid = session[USER_SESSION]["uid"]

    @staticmethod
    def add(_dict):
        #_dict["approval_uid"] = user_ldap.get_superior(_dict["uid"])
        leave = Leave(_dict)
        db.session.add(leave)
        db.session.commit()
        return leave

    @staticmethod
    def approval(submit):
        submit["approval_time"] = datetime.now().strftime("%Y-%m-%d")
        leave = Database.to_cls(Leave, submit)
        db.session.commit()
        return leave

    @staticmethod
    @db.transaction
    def delete(lid):
        leave = Leave.query.filter(Leave.id == lid).one()
        if leave.status:
            raise ExceptionEx("申请已审批,无法删除")

        db.session.delete(leave)
        db.session.flush()
        return True

    @staticmethod
    def _to_dict(self):
        _dict = self.to_dict()
        return _dict

    @staticmethod
    def unapprovaled(page=0, pre_page=None):
        return Leave.query \
            .filter(Leave.status.in_([None, ""])) \
            .order_by(Leave.id.desc())\
            .paginate(page, pre_page, False).to_page(Leave._to_dict)

    @staticmethod
    def select(page=0, pre_page=None):
        uid = session[USER_SESSION]["uid"]
        return Leave.query \
            .filter(Leave.uid == uid) \
            .paginate(page, pre_page, False).to_page(Leave._to_dict)

    @staticmethod
    def between(beg, end,is_history=False):
        if is_history:
            query=Leave.query.filter(Leave.status != None).filter(Leave.status != "")
        else:
            query=Leave.query.filter(Leave.status == LEAVE.PASS)


        return [Leave._to_dict(l) for l in query
            .filter(or_(
            and_(Leave.begin_time >= beg, Leave.end_time <= end, Leave.begin_time <= end, Leave.end_time >= beg),
            and_(Leave.begin_time <= beg, Leave.end_time >= beg),
            and_(Leave.begin_time <= end, Leave.end_time >= end))).all()]

    @staticmethod
    def history(page=0, pre_page=None):
        return Leave.query \
            .filter(Leave.status != None) \
            .filter(Leave.status != "") \
            .paginate(page, pre_page, False).to_page(Leave._to_dict)


class LeaveEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(128), default="", nullable=True)
    type_id = db.Column(db.Integer, db.ForeignKey("ref.id"))

    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    def __init__(self, _dict):
        for k, v in _dict.items():
            if "time" in k:
                setattr(self, k, datetime.strptime(v, "%Y-%m-%d"))
            else:
                setattr(self, k, v)

    @staticmethod
    def add(_dict):
        db.session.add(LeaveEvent(_dict))
        db.session.commit()
        return True

    @staticmethod
    def delete(leid):
        le = LeaveEvent.query.filter(LeaveEvent.id == leid).one()
        db.session.delete(le)
        db.session.commit()
        return True

    @staticmethod
    def select(page=0, pre_page=None):
        uid = session[USER_SESSION]["uid"]
        return Leave.query \
            .filter(or_(Leave.uid == uid, Leave.approval_uid == uid)) \
            .paginate(page, pre_page, False).to_page(Leave._to_dict)

    @staticmethod
    def _to_dict(self):
        _dict = self.to_dict()
        return _dict

    @staticmethod
    def between(beg, end):
        query = LeaveEvent.query \
            .filter(or_(
            and_(LeaveEvent.begin_time >= beg, LeaveEvent.end_time <= end, LeaveEvent.begin_time <= end,
                 LeaveEvent.end_time >= beg),
            and_(LeaveEvent.begin_time <= beg, LeaveEvent.end_time >= beg),
            and_(LeaveEvent.begin_time <= end, LeaveEvent.end_time >= end)))

        return [LeaveEvent._to_dict(l) for l in query.all()]


if __name__ == "__main__":
    from datetime import datetime

    LeaveEvent.between(datetime(2016, 1, 15), datetime(2016, 1, 15))
