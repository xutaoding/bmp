# coding=utf-8
from datetime import datetime
from datetime import timedelta

from flask import session

from bmp import db
from bmp.const import USER_SESSION, SCRAP, STOCK
from bmp.database import Database
from bmp.utils.exception import ExceptionEx
import bmp.utils.timeutil as time

from base import BaseModel


class Domain(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    sp = db.Column(db.String(128))
    end_time = db.Column(db.DateTime)


class Cert(BaseModel, db.Model):  # ssl证书
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    sp = db.Column(db.String(128))
    end_time = db.Column(db.DateTime)


# 主办单位  单位性质    网站备案/许可证号	网站名称    网站首页网址  审核时间  域名  ELB IP
class Icp(BaseModel, db.Model):  # 备案信息
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128))

    company = db.Column(db.String(128))
    company_type = db.Column(db.String(128))
    no = db.Column(db.String(128))
    site = db.Column(db.String(128))
    main_page = db.Column(db.String(128))
    chk_time = db.Column(db.DateTime)
    domain = db.Column(db.Text, default="")
    elb = db.Column(db.Text)
    ip = db.Column(db.Text)


class Supplier(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    connector = db.Column(db.String(128))
    interfaceor = db.Column(db.String(128))
    tel = db.Column(db.String(128))
    addr = db.Column(db.String(128))
    create_time = db.Column(db.DateTime)
    last_time = db.Column(db.DateTime)
    path = db.Column(db.String(256))


class Contract(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(128))
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))
    path = db.Column(db.String(256))  # 合同文件路径

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


class Category(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    parent_id = db.Column(db.Integer)
    is_del = db.Column(db.Boolean, default=False)

    @classmethod
    def add(cls, _dict):
        query = Category.query \
            .filter(Category.parent_id == _dict["parent_id"]) \
            .filter(Category.name == _dict["name"])

        if query.filter(Category.is_del == False).count():
            raise ExceptionEx("分类%s已经存在" % _dict["name"])

        if query.filter(Category.is_del == True).count():
            category = query.one()
            category.is_del = False
        else:
            db.session.add(Category(_dict))

        db.session.commit()
        return True

    @staticmethod
    def __delete(id):
        category = Category.query.filter(Category.parent_id == id)

        for child in category.all():
            Category.__delete(child.to_dict())

        category = Category.query.filter(Category.id == id).one()
        category.is_del = True

    @classmethod
    def delete(cls, id):
        Category.__delete(id)

    @staticmethod
    def __select_sub(parent_id):
        sub = []
        for c in Category.query \
                .filter(Category.is_del == False) \
                .filter(Category.parent_id == parent_id).all():
            c.child = Category.__select_sub(c.id)
            sub.append(c.to_dict(["child"]))
        return sub

    @staticmethod
    def select_sub(parent_id):
        return Category.__select_sub(parent_id)

    @staticmethod
    def get_parent_ids(_id):
        ids = []
        category = Category.query.filter(Category.id == _id).one()
        if not category.parent_id:
            return []
        ids.extend(Category.get_parent_ids(category.parent_id))
        return ids

    @staticmethod
    def get_child_ids(_id):
        categorys = Category.query.filter(Category.parent_id == _id).all()
        if not categorys:
            return []

        ids = [c.id for c in categorys]

        for category in categorys:
            ids.extend(Category.get_child_ids(category.id))
        return ids


stock_category = db.Table("stock_category",
                          db.Column("stock_id", db.Integer, db.ForeignKey("stock.id")),
                          db.Column("category_id", db.Integer, db.ForeignKey("category.id")))

stock_spec_category = db.Table("stock_spec_category",
                               db.Column("stock_id", db.Integer, db.ForeignKey("stock.id")),
                               db.Column("category_id", db.Integer, db.ForeignKey("category.id")))


class StockOpt(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(64))
    uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    time = db.Column(db.DateTime)
    reson = db.Column(db.String(128))
    remark = db.Column(db.String(128))
    status = db.Column(db.String(128))
    update_time = db.Column(db.DateTime)
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"))
    approval_uid = db.Column(db.String(128), db.ForeignKey("user.uid"), default="", nullable=True)
    approval_time = db.Column(db.DateTime, nullable=True)
    approval_remark = db.Column(db.String(128), nullable=True)

    def __init__(self, _dict):
        if not _dict.__contains__("id"):
            _dict["status"] = ""
        elif _dict["type"] == SCRAP.TYPE:
            _dict["approval_uid"] = session[USER_SESSION]["uid"]
            _dict["approval_time"] = datetime.now().strftime("%Y-%m-%d")
            _dict["update_time"] = datetime.now().strftime("%Y-%m-%d")
        else:
            _dict["update_time"] = datetime.now().strftime("%Y-%m-%d")

        if not _dict.__contains__("stock_id"):
            raise ExceptionEx("库存不能为空")
        elif not Stock.query.filter(Stock.id == _dict["stock_id"]).count():
            raise ExceptionEx("库存不存在")

        BaseModel.__init__(self, _dict)

    @staticmethod
    def _to_dict(self):
        stock = Stock._to_dict(self.stock, False)
        opt = self.to_dict()
        opt["stock"] = stock
        return opt

    @staticmethod
    def approvals(page, pre_page):  # todo 添加报废的审批组
        page = StockOpt.query \
            .filter(StockOpt.type == SCRAP.TYPE) \
            .filter(StockOpt.status.in_(["", SCRAP.PASS, SCRAP.FAIL])).paginate(page, pre_page)
        return page.to_page(StockOpt._to_dict)

    @staticmethod
    def search(submit, page=None, pre_page=None):
        from bmp.models.user import User
        from bmp.models.purchase import Purchase
        # 固定资产编号	入库时间	申请人	申请部门	物品类别	价格范围	物品状态
        def check(s):
            if submit.__contains__(s):
                return submit[s]
            return False

        query = StockOpt.query \
            .order_by(StockOpt.time.desc()) \
            .order_by(StockOpt.update_time.desc()) \
            .join(User, User.uid == StockOpt.uid) \
            .join(Stock, Stock.id == StockOpt.stock_id) \
            .join(stock_category) \
            .join(Category) \
            .filter(StockOpt.status.in_(["", SCRAP.TYPE]))

        if check("no"):
            query = query.filter(Stock.no == submit["no"])

        if check("stock_in_time_begin") and check("stock_in_time_end"):
            beg = datetime.strptime(submit["stock_in_time_begin"], "%Y-%m-%d")
            end = datetime.strptime(submit["stock_in_time_end"], "%Y-%m-%d")
            query = query.filter(Stock.stock_in_time.between(beg, end))

        if check("uid"):
            query = query.filter(User.uid == submit["uid"])

        if check("businessCategory"):
            query = query.filter(User.businessCategory == submit["businessCategory"])

        if check("category_id"):
            ids = Category.get_child_ids(submit["category_id"]) + [submit["category_id"]]
            query = query.filter(Category.id.in_(ids))

        if check("price_start") and check("price_end"):
            query = query \
                .join(Purchase, Purchase.id == Stock.purchase_id) \
                .filter(Purchase.goods.price.between(
                submit["price_start"], submit["price_end"]))

        if check("status"):
            query = query.filter(StockOpt.type == check("status"))

        if page == None:
            return [StockOpt._to_dict(p) for p in query.all()]

        return query.paginate(page, pre_page, False).to_page(StockOpt._to_dict)

    @staticmethod
    def export(submit):
        # 固定资产编号	入库时间	申请人	名称	状态	详细
        _export = []
        for stockopt in StockOpt.search(submit):
            _dict = {}
            stock = stockopt["stock"]
            _dict["状态"] = stockopt["status"]
            _dict["名称"] = stock["category"]["name"]
            _dict["申请人"] = stockopt["uid"]
            _dict["入库时间"] = time.format(stock["stock_in_time"], "%Y-%m-%d")
            _dict["固定资产编号"] = stock["no"]
            _export.append(_dict)
        return _export


class Stock(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    no = db.Column(db.String(128), unique=True)
    category = db.relationship("Category",
                               secondary=stock_category,
                               backref=db.backref("stocks"),
                               uselist=False)

    spec = db.relationship("Category",
                           secondary=stock_spec_category,
                           uselist=False)

    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))
    stock_in_type = db.Column(db.String(128))
    stock_in_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    stock_in_time = db.Column(db.DateTime)
    warranty_time = db.Column(db.DateTime)
    opts = db.relationship("StockOpt", backref=db.backref("stock"))

    @staticmethod
    def search(submit, page=None, pre_page=None):
        from bmp.models.user import User
        from bmp.models.purchase import Purchase

        def check(s):
            if submit.__contains__(s):
                return submit[s]
            return False

        query = Stock.query \
            .order_by(Stock.stock_in_time.desc()) \
            .join(stock_category) \
            .join(Category)

        if check("status"):
            if check("status") == STOCK.TYPE:
                stock_ids = [s.stock_id for s in StockOpt.query.filter(StockOpt.status.in_(["", SCRAP.TYPE])).all()]
                query = query.join(User, Stock.stock_in_uid == User.uid).filter(~Stock.id.in_(stock_ids))
            else:
                query = query \
                    .join(StockOpt, Stock.id == StockOpt.stock_id) \
                    .join(User, StockOpt.uid == User.uid) \
                    .filter(StockOpt.status.in_(["", SCRAP.TYPE])) \
                    .filter(StockOpt.type == check("status"))
        else:
            query = query.join(User, Stock.stock_in_uid == User.uid)

        if check("uid"):
            query = query.filter(User.uid == submit["uid"])

        if check("businessCategory"):
            query = query.filter(User.businessCategory == submit["businessCategory"])

        if check("no"):
            query = query.filter(Stock.no == submit["no"])

        if check("stock_in_time_begin") and check("stock_in_time_end"):
            beg = datetime.strptime(submit["stock_in_time_begin"], "%Y-%m-%d")
            end = datetime.strptime(submit["stock_in_time_end"], "%Y-%m-%d")
            query = query.filter(Stock.stock_in_time.between(beg, end))

        if check("warranty_time_begin") and check("warranty_time_end"):
            beg = datetime.strptime(submit["warranty_time_begin"], "%Y-%m-%d")
            end = datetime.strptime(submit["warranty_time_end"], "%Y-%m-%d")
            query = query.filter(Stock.stock_in_time.between(beg, end))

        if check("category_id"):
            ids = Category.get_child_ids(submit["category_id"]) + [submit["category_id"]]
            print(ids)
            query = query.filter(Category.id.in_(ids))

        if check("price_start") and check("price_end"):
            query = query \
                .join(Purchase, Purchase.id == Stock.purchase_id) \
                .filter(Purchase.goods.price.between(
                submit["price_start"], submit["price_end"]))

        if page == None:
            return [Stock._to_dict(p) for p in query.all()]

        return query.paginate(page, pre_page, False).to_page(Stock._to_dict)

    @staticmethod
    def export(submit):
        # 固定资产编号	入库时间	申请人	名称	状态	详细
        _export = []
        for stockopt in Stock.search(submit):
            _dict = {}
            stock = stockopt["stock"]
            _dict["名称"] = stock["category"]["name"]
            _dict["规格"] = stock["spec"]["name"]
            _dict["入库时间"] = time.format(stock["stock_in_time"], "%Y-%m-%d")
            _dict["固定资产编号"] = stock["no"]
            _export.append(_dict)
        return _export

    def __init__(self, _dict):
        BaseModel.__init__(self)

        for k, v in _dict.items():
            if k == "category_id":
                query = Category.query.filter(Category.id == v)
                if not query.count():
                    raise ExceptionEx("不存在的商品id")
                self.category = query.one()
            if k == "spec_id":
                query = Category.query.filter(Category.id == v)
                if not query.count():
                    raise ExceptionEx("不存在的规格id")
                self.spec = query.one()
            if "time" in k:
                setattr(self, k, datetime.strptime(v, "%Y-%m-%d"))
            elif k == "id":
                pass
            else:
                setattr(self, k, v)

    @classmethod
    def add(cls, _dict):
        '''
        固定资产编号 格式固定一下
        部门+年+月+0001
        比如：IT2015050001
        :param _dict:
        :return:
        '''
        if not _dict.__contains__("no") or Stock.query \
                .filter(Stock.no == _dict["no"]).count():
            raise ExceptionEx("库存编号已存在")

        if not _dict.__contains__("category_id"):
            raise ExceptionEx("名称不能为空")

        def create_no():
            businessCategory = session[USER_SESSION]["businessCategory"]
            today = datetime.strptime(_dict["stock_in_time"], "%Y-%m-%d")
            year, month = today.year, today.month
            beg = datetime(year, month, 1)
            if month == 12:
                end = datetime(year, month, 31)
            else:
                end = datetime(year, month + 1, 1) - timedelta(days=1)

            stocks = [int(s.no[-4:]) for s in Stock.query.filter(
                Stock.stock_in_time.between(beg, end)).all()]
            stocks.append(0)
            return "%s%d%02d%04d" % (businessCategory.upper(), year, month, max(stocks) + 1)

        _dict["no"] = create_no()
        stock = Stock(_dict)
        db.session.add(stock)
        db.session.commit()
        return stock

    @classmethod
    def edit(cls, _dict):
        if Stock.query.filter(Stock.no == _dict["no"]).count():
            raise ExceptionEx("库存编号已存在")

        stock = Database.to_cls(Stock, _dict)
        db.session.commit()
        return stock

    @staticmethod
    def _to_dict(self, show_opt=False):
        _dict = self.to_dict()
        category = self.category
        spec = self.spec
        _dict["status"] = ""

        if spec: _dict["spec"] = spec.to_dict()
        if category: _dict["category"] = category.to_dict()

        opts = self.opts
        for opt in opts:
            if opt.status.strip() in ["", SCRAP.TYPE]:
                _dict["status"] = opt.type

        if show_opt:
            _dict["opts"] = [opt.to_dict() for opt in opts]

        return _dict

    @classmethod
    def get(cls, _id, _filters=None):
        return Stock._to_dict(Stock.query.filter(Stock.id == id).one(), True)

    @classmethod
    def select(cls, page=None, pre_page=None, _filters=None, _orders=None):
        query = Stock.query.order_by(Stock.stock_in_time.desc())
        if _filters:
            opts = StockOpt.query.filter(StockOpt.status.in_(["", SCRAP.PASS, SCRAP.TYPE])).all()
            in_opts = [opt.stock_id for opt in opts]
            query = query.filter(~Stock.id.in_(in_opts))
        page = query.paginate(page, pre_page)
        return page.to_page(Stock._to_dict)


if __name__ == "__main__":
    db.session.add(Category({"name":"test","parent_id":0}))
