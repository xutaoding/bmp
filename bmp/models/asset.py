# coding=utf-8
from bmp import db
from flask import session
from bmp.const import USER_SESSION
from datetime import datetime
from bmp.database import Database

# 基础信息里的三张表
from datetime import datetime


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    connector = db.Column(db.String(128))
    interfaceor = db.Column(db.String(128))
    tel = db.Column(db.String(128))
    addr = db.Column(db.String(128))
    create_time = db.Column(db.DateTime)
    last_time = db.Column(db.DateTime)
    path = db.Column(db.String(256))

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
    @db.transaction
    def edit(id, _dict):
        supplier = Supplier.query.filter(Supplier.id == id).one()
        supplier.name = _dict["name"]
        supplier.connector = _dict["connector"]
        supplier.tel = _dict["tel"]
        supplier.addr = _dict["addr"]
        supplier.interfaceor = _dict["interfaceor"]
        # supplier.create_time = datetime.now()

        supplier.last_time = datetime.now()
        db.session.flush()
        return True

    @staticmethod
    def history():
        query = Supplier.query.order_by(Supplier.id.desc())
        return [supplier.to_dict() for supplier in query.all()]

    @staticmethod
    def get(sid):
        return Supplier.query.filter(Supplier.id == sid).one()


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))
    path = db.Column(db.String(256))  # 合同文件路径

    def __init__(self, _dict):
        if _dict["begin_time"]:
            self.begin_time = datetime.strptime(_dict["begin_time"], "%Y-%m-%d")
        else:
            self.begin_time = datetime.now()
        if _dict["end_time"]:
            self.end_time = datetime.strptime(_dict["end_time"], "%Y-%m-%d")
        else:
            self.end_time = datetime.now()

        self.path = _dict["path"]

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
    @db.transaction
    def edit(id, _dict):
        contract = Contract.query.filter(Contract.id == id).one()
        contract.begin_time = datetime.strptime(_dict["begin_time"], "%Y-%m-%d")
        contract.end_time = datetime.strptime(_dict["end_time"], "%Y-%m-%d")
        contract.purchase_id = _dict["purchase_id"]
        contract.path = _dict["path"]
        db.session.flush()
        return True

    @staticmethod
    def _to_dict(contract):
        _dict = contract.to_dict()
        from bmp.models.purchase import Purchase
        purchase = contract.purchase
        if purchase:
            purchase = Purchase._to_dict(purchase)
            purchase.pop("imgs")
            purchase.pop("contract")
            _dict["purchase"] = purchase
        return _dict

    @staticmethod
    def select():
        query = Contract.query.order_by(Contract.id.desc())
        return [Contract._to_dict(contract) for contract in query.all()]


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    parent_id = db.Column(db.Integer)

    def __init__(self, _dict):
        self.name = _dict["name"]
        self.parent_id = _dict["parent_id"]

    @staticmethod
    @db.transaction
    def add(_dict):
        if Category.query \
                .filter(Category.parent_id == _dict["parent_id"]) \
                .filter(Category.name == _dict["name"]).count():
            return False
        db.session.add(Category(_dict))
        db.session.flush()
        return True

    @staticmethod
    def edit(id, _dict):
        if Category.query \
                .filter(Category.parent_id == _dict["parent_id"]) \
                .filter(Category.name == _dict["name"]).count():
            return False
        category = Category.query.filter(Category.id == id).one()
        category.name = _dict["name"]
        category.parent_id = _dict["parent_id"]
        db.session.flush()
        return True

    @staticmethod
    def __delete(id):
        category = Category.query.filter(Category.parent_id == id)
        if category.count():
            for child in category.all():
                Category.__delete(child.to_dict())

        db.session.delete(Category.query.filter(Category.id == id).one())

    @staticmethod
    @db.transaction
    def delete(id):
        Category.__delete(id)

    @staticmethod
    @db.transaction
    def __select_sub(parent_id):
        sub = []
        for c in Category.query.filter(Category.parent_id == parent_id).all():
            c.child = Category.__select_sub(c.id)
            sub.append(c.to_dict(["child"]))
        return sub

    @staticmethod
    @db.transaction
    def select(parent_id):
        return Category.__select_sub(parent_id)

    @staticmethod
    @db.transaction
    def get_parent_ids(_id):
        ids = []
        category = Category.query.filter(Category.id == _id).one()
        if not category.parent_id:
            return []
        ids.extend(Category.get_parent_ids(category.parent_id))
        return ids

    @staticmethod
    @db.transaction
    def get_child_ids(_id):
        ids = []
        categorys = Category.query.filter(Category.parent_id == _id).all()
        if not categorys:
            return []
        for category in categorys:
            ids.extend(Category.get_child_ids(category.id))
        return ids


class StockOpt(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(64))
    uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    time = db.Column(db.DateTime)
    reson = db.Column(db.String(128))
    remark = db.Column(db.String(128))
    status = db.Column(db.String(128))
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"))

    def __init__(self, _dict):
        Stock.init(self, _dict)

    @staticmethod
    def add(_dict):
        db.session.add(StockOpt(_dict))
        db.session.commit()
        return True

    @staticmethod
    def edit(_dict):
        opt = Database.to_cls(StockOpt, _dict)
        db.session.commit()
        return True

    @staticmethod
    def delete(id):
        stockopt = StockOpt.query.filter(StockOpt.id == id).one()
        db.session.delete(stockopt)
        db.session.commit()
        return True

    @staticmethod
    def _to_dict(self):
        stock = self.stock.to_dict()
        opt = self.to_dict()
        opt["stock"] = stock
        return opt

    @staticmethod
    def select(type, page, pre_page):
        page = StockOpt.query.filter(StockOpt.type == type).paginate(page, pre_page)
        return page.to_page(StockOpt._to_dict)

    @staticmethod
    def get(type, id):
        return StockOpt.query \
            .filter(StockOpt.type == type) \
            .filter(StockOpt.id == id).one().to_dict()


stock_category = db.Table("stock_category",
                          db.Column("stock_id", db.Integer, db.ForeignKey("stock.id")),
                          db.Column("category_id", db.Integer, db.ForeignKey("category.id")))


class Stock(db.Model):
    # 固定资产编号	采购编号	名称	规格	入库类型	入库人	入库时间	过保日
    # 操作人	操作时间	备注	状态

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    no = db.Column(db.String(128), unique=True)
    category = db.relationship("Category",
                               secondary=stock_category,
                               backref=db.backref("stocks"),
                               uselist=False)

    spec = db.Column(db.String(128))
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))
    stock_in_type = db.Column(db.Integer,db.ForeignKey("ref.id"))
    stock_in_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    stock_in_time = db.Column(db.DateTime)
    warranty_time = db.Column(db.DateTime)
    opts = db.relationship("StockOpt", backref=db.backref("stock"))

    @staticmethod
    def init(self, _dict):
        for k, v in _dict.items():
            if k == "category_id":
                self.category = Category.query.filter(Category.id == v).one()
            elif "time" in k:
                setattr(self, k, datetime.strptime(v, "%Y-%m-%d %H:%M"))
            elif k == "id":
                pass
            else:
                setattr(self, k, v)

    def __init__(self, _dict):
        Stock.init(self, _dict)

    @staticmethod
    @db.transaction
    def add(_dict):
        if Stock.query \
                .filter(Stock.no == _dict["no"]).count():
            raise Exception("库存编号已存在")

        db.session.add(Stock(_dict))
        db.session.flush()
        return True

    @staticmethod
    @db.transaction
    def edit(_dict):
        if Stock.query.filter(Stock.no == _dict["no"]).count():
            raise Exception("库存编号已存在")

        stock = Database.to_cls(Stock, _dict)
        db.session.flush()

    @staticmethod
    def delete(id):
        stock = Stock.query.filter(Stock.id == id).one()
        db.session.delete(stock)
        db.session.commit()

    @staticmethod
    def _to_dict(self):
        _dict = self.to_dict()
        _dict["category_id"] = self.category.id
        _dict["opts"] = [opt.to_dict() for opt in self.opts]
        return _dict

    @staticmethod
    def get(id):
        return Stock.query.filter(Stock.id == id).one().to_dict()

    @staticmethod
    def select(page, pre_page):
        page = Stock.query.paginate(page, pre_page)
        return page.to_page(Stock._to_dict)

    @staticmethod
    def search(submit, page=None, pre_page=None):
        from bmp.models.user import User
        from bmp.models.purchase import Purchase, PurchaseGoods
        # 固定资产编号	入库时间	申请人	申请部门	物品类别	价格范围	物品状态
        def check(s):
            if submit.__contains__(s):
                return submit[s]
            return False

        query = Stock.query \
            .join(StockOpt, Stock.id == StockOpt.stock_id) \
            .join(stock_category) \
            .join(Category)

        if check("no"):
            query = query.filter(Stock.no == submit["no"])

        if check("stock_in_time_begin") and check("stock_in_time_end"):
            beg = datetime.strptime(submit["stock_in_time_begin"], "%Y-%m-%d %H:%M")
            end = datetime.strptime(submit["stock_in_time_end"], "%Y-%m-%d %H:%M")
            query = query.filter(Stock.stock_in_time.between(beg, end))

        if check("uid"):
            query = query.filter(User.uid == submit["uid"])

        if check("businessCategory"):
            query = query.filter(User.businessCategory == submit["businessCategory"])

        if check("category_id"):
            ids = Category.get_child_ids(submit["category_id"]) + [submit["category_id"]]
            query = query.filter(Category.id.in_(ids))

        if check("price_start") and check("price_end"):
            query.join(Purchase, Purchase.id == Stock.purchase_id)
            start = check("price_start")
            end = check("price_end")
            query = query.filter(Purchase.goods.price.between(start, end))

        if check("status"):
            query = query.filter(StockOpt.type == check("status"))

        if page == None:
            return [Stock._to_dict(p) for p in query.all()]
        return query.paginate(page, pre_page, False).to_page(Stock._to_dict)

    @staticmethod
    def export(submit):
        # 固定资产编号	入库时间	申请人	名称	状态	详细
        _export = []
        for stock in Stock.search(submit):
            _dict = {}
            _dict["状态"] = stock["status"]
            _dict["名称"] = stock["category"]["name"]
            _dict["申请人"] = stock["apply_uid"]
            _dict["入库时间"] = stock["apply_time"].strftime("%Y-%m-%d %H:%M")
            _dict["固定资产编号"] = stock["no"]
            _export.append(_dict)
        return _export


if __name__ == "__main__":
    pass
