#coding=utf-8
from bmp import db
from flask import session
from bmp.models.user import User
from bmp.const import USER_SESSION
from datetime import datetime

purchase_supplier = db.Table("purchase_supplier",
                             db.Column("purchase_id", db.Integer, db.ForeignKey("purchase.id")),
                             db.Column("supplier_id", db.Integer, db.ForeignKey("supplier.id")))


class PurchaseGoods(db.Model):  # 采购物品
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Float)
    spec = db.Column(db.String(128))
    amount = db.Column(db.Integer)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))

class PurchaseImg(db.Model):  # 比价图片
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    b64 = db.Column(db.String(256))
    desc = db.Column(db.String(128))
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))

class PurchaseApproval(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128))
    uid = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(128), nullable=False)
    reson = db.Column(db.String(128))
    options = db.Column(db.String(128))
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    approvals = db.relationship("PurchaseApproval")
    contract = db.relationship("Contract",uselist=False)
    imgs = db.relationship("PurchaseImg")
    goods = db.relationship("PurchaseGoods")
    supplier = db.relationship("Supplier",
                               secondary=purchase_supplier,
                               backref=db.backref("purchases"),
                               uselist=False)
    use=db.Column(db.String(128))
    apply_uid = db.Column(db.String(128), nullable=False)
    apply_time = db.Column(db.DateTime, nullable=False)

    def __init__(self,goods,supplier,imgs=None,contract=None):
        self.apply_uid=session[USER_SESSION]["uid"]
        self.apply_time=datetime.now()
        self.goods=goods
        self.supplier=supplier
        if imgs:self.imgs=imgs
        if contract:self.contract=contract

    @staticmethod
    def add(submit):
        imgs,contract=None,None
        if submit.__contains__("contract"):contract=submit["contract"]
        purchase=Purchase(submit["goods"],submit["supplier"],imgs,contract)
        purchase.use=submit["use"]
        db.session.add(purchase)
        db.session.commit()

    @staticmethod
    def select(id=0):
        return Purchase.query.all()


    @staticmethod
    def page(page=1,pre_page=20):
        return Purchase.query.paginate(page,pre_page,False)


if __name__ == "__main__":
    pass
