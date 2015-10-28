# coding=utf-8
from bmp import db
from flask import session
from bmp.const import USER_SESSION
from datetime import datetime

# 基础信息里的三张表
from datetime import datetime
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    connector = db.Column(db.String(128))
    tel = db.Column(db.String(128))
    addr = db.Column(db.String(128))
    interfaceor = db.Column(db.String(128))
    create_time = db.Column(db.DateTime)
    last_time = db.Column(db.DateTime)


    def __init__(self, _dict):
        for key, value in _dict.items():
            setattr(self, key, value)

    @staticmethod
    def add(_dict):
        # from bmp.models.user import User
        # user = User.query.filter(User.uid == session[USER_SESSION].uid).one()

        new_supplier = Supplier(_dict)
        # new_supplier.interfaceor = user.uid
        new_supplier.create_time = datetime.now()
        new_supplier.last_time = datetime.now()
        db.session.add(new_supplier)
        db.session.commit()
        return True

    @staticmethod
    def delete(id):
        supplier = Supplier.query.filter(Supplier.id == id).one()
        db.session.delete(supplier)
        db.session.commit()
        return True

    @staticmethod
    def edit(id, _dict):
        supplier = Supplier.query.filter(Supplier.id == id).one()
        supplier.id = _dict["id"]
        supplier.name = _dict["name"]
        supplier.connector = _dict["connector"]
        supplier.tel = _dict["tel"]
        supplier.addr = _dict["addr"]
        supplier.interfaceor = _dict["interfaceor"]
        supplier.create_time = datetime.now()
        supplier.last_time = datetime.now()
        db.session.flush()
        return True

    @staticmethod
    def history():
        query = Supplier.query.order_by(Supplier.id.desc())
        return [supplier.to_dict() for supplier in query.all()]

    # @staticmethod
    # def get(id):
    #     return Supplier.query.filter(Supplier.id==id).one()


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    begin_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)


    path = db.Column(db.String(256))  # 合同文件路径
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))

    def __init__(self,_dict):
        self.begin_time=datetime.strptime(_dict["begin_time"],"%Y-%m-%d %H:%M")
        self.end_time=datetime.strptime(_dict["end_time"],"%Y-%m-%d %H:%M")
        self.path=_dict["path"]





if __name__=="__main__":
    from bmp.models.purchase import Purchase
    from bmp import db
    d=Contract({
                 "id":"2",
                 "begin_time":"2015-01-01 01:01",
                 "end_time":"2015-01-02 01:01",
                 "path":"合同文件路径2"
             })
    db.session.commit()
    print(d)



    def __init__(self,_dict):
        self.begin_time=_dict["begin_time"]
        self.end_time=_dict["end_time"]
        self.path=_dict["path"]

#
# class CategoryOne(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # parent_id=db.Column(db.Integer)
#     # name=db.Column(db.String(128))
#     sub_id = db.relationship("CategoryTwo")
#
#
# class CategoryTwo(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     categoryone_id = db.Column(db.Integer, db.ForeignKey("CategoryOne.id"))
#     sub_id = db.relationship("CategoryThree")
#
# class CategoryThree(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     categorytwo_id = db.Column(db.Integer, db.ForeignKey("CategoryTwo.id"))
#
#
#
#
