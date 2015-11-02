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

    @staticmethod
    def get(sid):
        return Supplier.query.filter(Supplier.id==sid).one()


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))
    path = db.Column(db.String(256))  # 合同文件路径

    def __init__(self,_dict):
        if _dict["begin_time"]:
            self.begin_time=datetime.strptime(_dict["begin_time"],"%Y-%m-%d")
        if _dict["end_time"]:
            self.end_time=datetime.strptime(_dict["end_time"],"%Y-%m-%d")
        self.path=_dict["path"]

    @staticmethod
    def add(_dict):
        db.session.add(Contract(_dict))
        db.session.commit()
        return True

    @staticmethod
    def delete(id):
        contract = Contract.query.filter(Contract.id == id).one()
        db.session.delete(contract)
        db.session.commit()
        return True

    @staticmethod
    def edit(id, _dict):
        contract = Contract.query.filter(Contract.id == id).one()
        contract.begin_time = _dict["begin_time"]
        contract.end_time = _dict["end_time"]
        contract.purchase_id = _dict["purchase_id"]
        contract.supplier_name = _dict["supplier_name"]
        contract.path = _dict["path"]
        db.session.flush()
        return True

    @staticmethod
    def history():
        query = Contract.query.order_by(Contract.id.desc())
        return [contract.to_dict() for contract in query.all()]


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    parent_id = db.Column(db.Integer)


    @staticmethod
    def add(_dict):
        db.session.add(Category(_dict))
        db.session.commit()
        return True

    @staticmethod
    def edit(id,_dict):
        category = Category.query.filter(Category.id==id).one()
        category.name = _dict["name"]
        category.parent_id = _dict["parent_id"]
        db.session.commit()
        return True


    @staticmethod
    def __delete(_dict):
        category=Category.query.filter(Category.parent_id==_dict["id"])
        if category.count():
            for child in category.all():
                Category.__delete(child.to_dict())
        db.session.delete(Category.query.filter(Category.id==_dict["id"]).one())

    @staticmethod
    @db.transaction
    def delete(_dict):
        Category.__delete(_dict)


if __name__=="__main__":
    _dict={"id":2}
    Category.delete(_dict)



'''
    from bmp.models.purchase import Purchase
    from bmp import db
    d=Contract({
                 "id":"2",
                 "begin_time":"2015-01-01 01:01",
                 "end_time":"2015-01-02 01:01",
                 "purchase_id":"1",
                 "supplier_name":"联想",
                 "path":"合同文件路径2"
             })
    db.session.commit()
    print(d)



    def __init__(self,_dict):
        self.begin_time=_dict["begin_time"]
        self.end_time=_dict["end_time"]
        self.path=_dict["path"]
'''
