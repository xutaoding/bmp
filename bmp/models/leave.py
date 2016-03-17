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

from base import BaseModel


class Leave(BaseModel,db.Model):
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
    def approval(submit):
        submit["approval_time"] = datetime.now().strftime("%Y-%m-%d")
        leave = Database.to_cls(Leave, submit)
        db.session.commit()
        return leave

    @classmethod
    @db.transaction
    def delete(cls,lid):
        leave = Leave.query.filter(Leave.id == lid).one()
        if leave.status:
            raise ExceptionEx("申请已审批,无法删除")

        db.session.delete(leave)
        db.session.flush()
        return True

    @staticmethod
    def unapprovaled(page=0, pre_page=None):
        return Leave.query \
            .filter(Leave.status.in_([None, ""])) \
            .order_by(Leave.id.desc()) \
            .paginate(page, pre_page, False).to_page(Leave._to_dict)

    @staticmethod
    def between(beg, end, query_type=False):
        query = Leave.query \
            .filter(Leave.status == LEAVE.PASS).filter(or_(
            and_(Leave.begin_time >= beg, Leave.end_time <= end, Leave.begin_time <= end, Leave.end_time >= beg),
            and_(Leave.begin_time <= beg, Leave.end_time >= beg),
            and_(Leave.begin_time <= end, Leave.end_time >= end)))

        if query_type:
            return query

        return [Leave._to_dict(l) for l in query.all()]

    @staticmethod
    def history(page=0, pre_page=None):
        return Leave.query \
            .filter(Leave.status != None) \
            .filter(Leave.status != "") \
            .paginate(page, pre_page, False).to_page(Leave._to_dict)

    @staticmethod
    def search(begin_time, end_time, name):
        query = Leave.between(begin_time, end_time, query_type=True) \
            .filter(Leave.approval_uid.ilike("%" + name + "%"))

        return [Leave._to_dict(l) for l in query.all()]





class LeaveEvent(BaseModel,db.Model):
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


if __name__ == "__main__":
    from datetime import datetime

    LeaveEvent.between(datetime(2016, 1, 15), datetime(2016, 1, 15))
