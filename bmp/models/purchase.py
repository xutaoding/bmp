#coding=utf-8
from bmp import db
from flask import session
from bmp.const import USER_SESSION
from datetime import datetime
from bmp.const import PURCHASE
import bmp.utils.user_ldap as ldap
from bmp.database import Database

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

    def __init__(self,_dict):
        self.name=_dict["name"]
        self.price=_dict["price"]
        self.spec=_dict["spec"]
        self.amount=_dict["amount"]

class PurchaseImg(db.Model):  # 比价图片
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    b64 = db.Column(db.Text)
    desc = db.Column(db.String(128))
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))

    def __init__(self,_dict):
        self.b64=_dict["b64"]
        self.desc=_dict["desc"]

class PurchaseApproval(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128))
    uid = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(128), nullable=False)
    reson = db.Column(db.String(128))
    options = db.Column(db.String(128))
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))

    def __init__(self,_dict):
        self.type=_dict["type"]
        self.status=_dict["status"]
        self.reson=_dict["reson"]
        self.options=_dict["options"]
        self.uid=_dict["uid"]


    @staticmethod
    def __next_approval_type(type):
        cur=PURCHASE.FLOW.index(type)
        if cur==len(PURCHASE.FLOW)-1:
            return PURCHASE.FLOW[cur]
        return PURCHASE.FLOW[cur+1]

    @staticmethod
    @db.transaction
    def edit(id,submit):
        approval=PurchaseApproval.query\
            .filter(PurchaseApproval.purchase_id==id)\
            .filter(PurchaseApproval.type==submit["type"])
        if approval.count():
            return False

        _approval=PurchaseApproval(submit)
        purchase=Purchase.query.filter(Purchase.id==id).one()
        purchase.approvals.append(_approval)

        #失败
        if _approval.status is PURCHASE.FAIL:
            purchase.is_finished=True
        else:
            if _approval.type is PURCHASE.FLOW_TWO:
                total=sum([g.price*g.amount for g in Purchase.goods])
                if total<PURCHASE.PRICE_LIMIT:
                    purchase.is_finished=True
            elif _approval.type is PURCHASE.FLOW_THREE:
                if not purchase.contract:
                    purchase.is_finished=True
            elif _approval.type is PURCHASE.FLOW_FOUR:
                purchase.is_finished=True

        purchase.cur_approval_type=PurchaseApproval.__next_approval_type(_approval.type)

        db.session.flush()
        return True

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    approvals = db.relationship("PurchaseApproval")
    contract = db.relationship("Contract",uselist=False,backref=db.backref("purchase"))
    imgs = db.relationship("PurchaseImg")
    goods = db.relationship("PurchaseGoods")
    supplier = db.relationship("Supplier",
                               secondary=purchase_supplier,
                               backref=db.backref("purchases"),
                               uselist=False)

    cur_approval_type=db.Column(db.String(128))
    is_finished=db.Column(db.Boolean,default=False)
    is_draft=db.Column(db.Boolean,default=True)
    use=db.Column(db.String(128))
    apply_uid = db.Column(db.String(128), nullable=False)
    apply_businessCategory=db.Column(db.String(128),nullable=False)
    apply_time = db.Column(db.DateTime, nullable=False)

    def __init__(self,submit):
        goods,supplier,imgs,contract=submit["goods"],submit["supplier"],submit["imgs"],submit["contract"]
        if not submit.__contains__("id"):
            self.cur_approval_type=PURCHASE.FLOW_ONE
            self.apply_time=datetime.now()
            self.apply_businessCategory=session[USER_SESSION]["businessCategory"]
            self.apply_uid=session[USER_SESSION]["uid"]

        self.goods=[Database.to_cls(PurchaseGoods,g) for g in goods]
        self.supplier=supplier
        if imgs:self.imgs=[Database.to_cls(PurchaseImg,img) for img in imgs]
        if contract:self.contract=contract
        self.use=submit["use"]

    @staticmethod
    @db.transaction
    def add(submit):
        purchase=Purchase(submit)
        db.session.add(purchase)
        db.session.flush()

    @staticmethod
    def get(id):
        return Purchase.to_dict(Purchase.query.filter(Purchase.id==id).one())

    @staticmethod
    def _to_dict(self,cols=[]):
        _dict=self.to_dict(cols)
        _dict["approvals"]=[ a.to_dict() for a in self.approvals]
        if self.contract:
            _dict["contract"]=self.contract.to_dict()
        _dict["imgs"]=[img.to_dict() for img in self.imgs]
        _dict["goods"]=[g.to_dict() for g in self.goods]
        _dict["supplier"]=self.supplier.to_dict()
        return _dict

    @staticmethod
    def __is_superior(uid,apply_uid):
        if uid==ldap.get_superior(apply_uid):
            return True
        if uid=="mingming.zhang":
            return  True


        return False

    @staticmethod
    def unfinished(user_groups):
        purchases=[]
        uid=session[USER_SESSION]["uid"]

        for purchase in Purchase.query\
                .filter(Purchase.is_draft==False)\
                .filter(Purchase.is_finished==False).order_by(Purchase.apply_time.desc()).all():

            approvals=purchase.approvals
            apply_uid=purchase.apply_uid
            cur_approval_type=purchase.cur_approval_type
            purchase.approval_enable=False

            if cur_approval_type==PURCHASE.FLOW_ONE:
                if Purchase.__is_superior(uid,apply_uid):
                    purchase.approval_enable=True
                    purchases.append(purchase)
            elif uid in user_groups[cur_approval_type]:
                purchase.approval_enable=True
                purchases.append(purchase)
            elif uid==purchase.apply_uid:
                purchases.append(purchase)
            elif uid in [a.uid for a in approvals]:
                purchases.append(purchase)
            else:
                continue
        return [Purchase._to_dict(p,["approval_enable"]) for p in purchases]

    @staticmethod
    def finished(page=1,pre_page=20):
        page=Purchase.query.filter(Purchase.is_finished==True).paginate(page,pre_page,False)
        return page.to_page(Purchase.to_dict)

    @staticmethod
    def drafts(page=1,pre_page=20):
        page=Purchase.query\
            .filter(Purchase.apply_uid==session[USER_SESSION]["uid"])\
            .filter(Purchase.is_draft==True)\
            .order_by(Purchase.apply_time.desc())\
            .paginate(page,pre_page,False)
        return page.to_page(Purchase.to_dict)

    @staticmethod
    @db.transaction
    def delete(pid):
        db.session.delete(Purchase.query.filter(Purchase.id==pid).one())
        db.session.flush()

    @staticmethod
    @db.transaction
    def edit(submit):
        purchase=Database.to_cls(Purchase,submit)
        db.session.flush()

    @staticmethod
    def approval(pid):
        purchase=Purchase.query.filter(Purchase.id==pid).one()
        purchase.is_draft=False
        db.session.commit()
        return True




    @staticmethod
    def search(submit,page,pre_page):
        def check(s):
            if submit.__contains__(s):
                return submit[s]
            return False

        query=Purchase.query.join(PurchaseGoods,PurchaseGoods.purchase_id==Purchase.id)
        if check("apply_businessCategory"):
            query=query.filter(Purchase.apply_businessCategory==submit["apply_businessCategory"])
        if  check("apply_uid"):
            query=query.filter(Purchase.apply_uid==submit["apply_uid"])
        if check("apply_time_begin") and check("apply_time_end"):
            beg=datetime.strptime(submit["apply_time_begin"],"%Y-%m-%d")
            end=datetime.strptime(submit["apply_time_end"],"%Y-%m-%d")
            query=query.filter(Purchase.apply_time.between(beg,end))

        if check("goods"):
            query=query.filter(PurchaseGoods.name==submit["goods"])
        if check("price"):
            query=query.filter(PurchaseGoods.price==submit["price"])
        return query.paginate(page,pre_page,False).to_page(Purchase.to_dict)

if __name__ == "__main__":
    pass
