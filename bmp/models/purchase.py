#coding=utf-8
from bmp import db
from flask import session
from bmp.const import USER_SESSION
from datetime import datetime
from bmp.const import PURCHASE
from bmp.models.user import Group


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
    b64 = db.Column(db.String(256))
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
    def edit(id,submit):
        db.session.begin()
        try:

            approval=PurchaseApproval.query.filter(
                PurchaseApproval.purchase_id==id,
                PurchaseApproval.type==submit["type"])
            if approval.count():
                return False

            _approval=PurchaseApproval(submit)
            _approval.puchase_id=id
            db.session.add(_approval)

            purchase=Purchase.query.filter(Purchase.id==id).one()
            #失败
            if _approval.status is PURCHASE.FAIL:
                purchase.is_finished=True
            elif _approval.status is PURCHASE.FLOW_TWO:
                total=sum([g.price*g.amount for g in Purchase.goods])
                if total<PURCHASE.PRICE_LIMIT:
                    purchase.is_finished=True
            elif _approval.status is PURCHASE.FLOW_THREE:
                if not purchase.contract:
                    purchase.is_finished=True
            elif _approval.status is PURCHASE.FLOW_FOUR:
                purchase.is_finished=True

            db.session.commit()
        except:
            db.session.rollback()
            raise

        return True

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

    cur_approval_type=db.Column(db.String(128))
    is_finished=db.Column(db.Boolean,default=False)
    use=db.Column(db.String(128))
    apply_uid = db.Column(db.String(128), nullable=False)
    apply_time = db.Column(db.DateTime, nullable=False)

    def __init__(self,goods,supplier,imgs=None,contract=None):
        self.apply_uid=session[USER_SESSION]["uid"]
        self.apply_time=datetime.now()
        self.goods=[PurchaseGoods(g) for g in goods]
        self.supplier=supplier
        if imgs:self.imgs=[PurchaseImg(img) for img in imgs]
        if contract:self.contract=contract

    @staticmethod
    def add(submit):
        purchase=Purchase(
            submit["goods"],
            submit["supplier"],
            submit["imgs"],
            submit["contract"])

        purchase.use=submit["use"]
        db.session.add(purchase)
        db.session.commit()

    @staticmethod
    def select(id=0):
        return Purchase.query.all()

    @staticmethod
    def get(id):
        return Purchase.query.filter(Purchase.id==id).one()

    @staticmethod
    def __to_dict(self):
        _dict=self.to_dict()
        _dict["approvals"]=[ a.to_dict() for a in self.approvals]
        _dict["contract"]=self.contract.to_dict()
        _dict["imgs"]=[img.to_dict() for img in self.imgs]
        _dict["goods"]=[g.to_dict() for g in self.goods]
        _dict["supplier"]=self.supplier.to_dict()
        return _dict

    @staticmethod
    def __is_superior(uid,apply_uid):
        return True

    @staticmethod
    def __cur_approval_type(approvals):
        diff=set(PURCHASE.FLOW).difference([a.type for a in approvals])
        return PURCHASE.FLOW[min([ PURCHASE.FLOW.index(d) for d in diff])]

    @staticmethod
    def __unfinished():
        purchases=[]
        uid=session[USER_SESSION]["uid"]

        g_dict={}
        for g in set(PURCHASE.FLOW).difference(PURCHASE.FLOW_ONE):
            g_dict[g]=[user.uid for user in Group.get_users(g)]

        for purchase in Purchase.query.filter(Purchase.is_finished==False).all():
            approvals=purchase.approvals
            apply_uid=purchase.apply_uid

            #参与过审批
            if uid in [a.uid for a in approvals]:
                purchases.append(purchase.id)
                continue

            cur_approval_type=Purchase.__cur_approval_type(approvals)
            if cur_approval_type is PURCHASE.FLOW_ONE:
                #直接上级
                if Purchase.__is_superior(uid,apply_uid):
                    purchases.append(purchase.id)
                    continue
            if uid in g_dict[cur_approval_type]:
                return purchase.append(purchase.id)

            return True
        return purchases

    #全部可审批和历史审批
    @staticmethod
    def unfinished(page=1,pre_page=20):
        page=Purchase.query.filter(Purchase.id.in_(Purchase.__unfinished())).paginate(page,pre_page,False)
        return page.to_page(Purchase.__to_dict)

    @staticmethod
    def delete(pid):
        db.session.delete(Purchase.query.filter(Purchase.id==pid).one())
        db.session.commit()

if __name__ == "__main__":
    pass
