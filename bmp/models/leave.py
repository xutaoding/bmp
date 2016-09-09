# coding=utf-8

from sqlalchemy import or_, and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from base import BaseModel
from bmp import db
from bmp.const import LEAVE


class Leave(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    reson = db.Column(db.String(128))
    type_id = db.Column(db.Integer, db.ForeignKey("ref.id"))
    dept = db.Column(db.String(128))
    days = db.Column(db.Float)
    tel = db.Column(db.String(128))

    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    apply_time = db.Column(db.DateTime)

    status = db.Column(db.String(128), nullable=False)
    feedback = db.Column(db.String(128), nullable=True)

    copy_to_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    approval_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    approval_time = db.Column(db.DateTime)

    @staticmethod
    def check_overlap(submit):
        try:
            leave = Leave(submit)
            beg, end = leave.begin_time, leave.end_time

            return True if Leave.query \
                .filter(~Leave.status.like(LEAVE.FAIL)) \
                .filter(Leave.uid.like(leave.uid)).filter(or_(
                and_(Leave.begin_time >= beg, Leave.end_time <= end, Leave.begin_time <= end, Leave.end_time >= beg),
                and_(Leave.begin_time <= beg, Leave.end_time >= beg),
                and_(Leave.begin_time <= end, Leave.end_time >= end))).one() else False
        except NoResultFound:
            return False
        except MultipleResultsFound:
            return True

    @staticmethod
    def unapprovaled(page=0, pre_page=None):
        return Leave.query \
            .filter(Leave.status.in_([None, ""])) \
            .order_by(Leave.id.desc()) \
            .paginate(page, pre_page, False).to_page(Leave._to_dict)

    @staticmethod
    def between(beg, end):
        beg += " 00:00:00"
        end += " 23:59:59"

        query = Leave.query \
            .filter(Leave.status == LEAVE.PASS) \
            .filter(or_(
                and_(Leave.begin_time >= beg,
                     Leave.end_time <= end,
                     Leave.begin_time <= end,
                     Leave.end_time >= beg),
                and_(Leave.begin_time <= beg, Leave.end_time >= beg),
                and_(Leave.begin_time <= end, Leave.end_time >= end))
            ).order_by(Leave.apply_time.desc())

        return query

    @staticmethod
    def history(page=0, pre_page=None):
        return Leave.query \
            .filter(Leave.status != None) \
            .filter(Leave.status != "") \
            .paginate(page, pre_page, False).to_page(Leave._to_dict)

    @staticmethod
    def search(begin_time, end_time, name):
        query = Leave.between(begin_time, end_time) \
            .filter(Leave.uid.ilike("%" + name + "%"))

        return [Leave._to_dict(l) for l in query.all()]


class LeaveEvent(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(128), default="", nullable=True)
    type_id = db.Column(db.Integer, db.ForeignKey("ref.id"))

    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    @staticmethod
    def between(beg, end):
        query = LeaveEvent.query \
            .filter(or_(
            and_(LeaveEvent.begin_time >= beg, LeaveEvent.end_time <= end, LeaveEvent.begin_time <= end,
                 LeaveEvent.end_time >= beg),
            and_(LeaveEvent.begin_time <= beg, LeaveEvent.end_time >= beg),
            and_(LeaveEvent.begin_time <= end, LeaveEvent.end_time >= end)))

        return [LeaveEvent._to_dict(l) for l in query.all()]
