#coding=utf-8
from bmp import db


class Supplier(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(128),nullable=False,unique=True)
    tel=db.Column(db.String(128))
    addr=db.Column(db.String(128))
    price=db.Column(db.String(128))
    status=db.Column(db.String(128))

    @staticmethod
    def get(id):
        return Supplier.query.filter(Supplier.id==id).one()


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    begin_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    path = db.Column(db.String(256))  # 合同文件路径
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))

    def __init__(self,_dict):
        self.begin_time=_dict["begin_time"]
        self.end_time=_dict["end_time"]
        self.path=_dict["path"]
