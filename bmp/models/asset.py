# coding=utf-8
from datetime import datetime
from datetime import timedelta

from flask import session

from bmp import db
from bmp.const import USER_SESSION, SCRAP, STOCK
from bmp.database import Database
from bmp.utils.exception import ExceptionEx
import bmp.utils.time as time


class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    sp = db.Column(db.String(128))
    end_time = db.Column(db.DateTime)

    def __init__(self, _dict):
        for k, v in _dict.items():
            if "time" in k:
                setattr(self, k, datetime.strptime(v, "%Y-%m-%d"))
            else:
                setattr(self, k, v)

    @staticmethod
    def add(_dict):
        domain = Domain(_dict)
        db.session.add(domain)
        db.session.commit()
        return domain

    @staticmethod
    @db.transaction
    def delete(dids):
        if not isinstance(dids, list):
            dids = [dids]

        for did in dids:
            domain = Domain.query.filter(Domain.id == did).one()
            db.session.delete(domain)
        db.session.flush()
        return True

    @staticmethod
    def _to_dict(domain):
        return domain.to_dict()

    @staticmethod
    def select():
        return [Domain._to_dict(d) for d in Domain.query.all()]

    @staticmethod
    def get(did):
        return Domain._to_dict(Domain.query.filter(Domain.id == did).one())

    @staticmethod
    @db.transaction
    def edit(_dicts):
        if isinstance(_dicts, dict):
            _dicts = [_dicts]
        domains = [Database.to_cls(Domain, _dict) for _dict in _dicts]
        db.session.flush()
        return domains


class Cert(db.Model):  # ssl证书
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    sp = db.Column(db.String(128))
    end_time = db.Column(db.DateTime)

    def __init__(self, _dict):
        for k, v in _dict.items():
            if "time" in k:
                setattr(self, k, datetime.strptime(v, "%Y-%m-%d"))
            else:
                setattr(self, k, v)

    @staticmethod
    def add(_dict):
        cert = Cert(_dict)
        db.session.add(cert)
        db.session.commit()
        return cert

    @staticmethod
    @db.transaction
    def delete(dids):
        if not isinstance(dids, list):
            dids = [dids]

        for did in dids:
            cert = Cert.query.filter(Cert.id == did).one()
            db.session.delete(cert)
        db.session.flush()
        return True

    @staticmethod
    def _to_dict(cert):
        return cert.to_dict()

    @staticmethod
    def select():
        return [Cert._to_dict(d) for d in Cert.query.all()]

    @staticmethod
    def get(did):
        return Cert._to_dict(Cert.query.filter(Cert.id == did).one())

    @staticmethod
    @db.transaction
    def edit(_dicts):
        if isinstance(_dicts, dict):
            _dicts = [_dicts]
        certs = [Database.to_cls(Cert, _dict) for _dict in _dicts]
        db.session.flush()
        return certs


# 主办单位  单位性质    网站备案/许可证号	网站名称	网站首页网址	审核时间  域名  ELB IP
class Icp(db.Model):  # 备案信息
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128))

    company = db.Column(db.String(128))
    company_type = db.Column(db.String(128))
    no = db.Column(db.String(128))
    site = db.Column(db.String(128))
    main_page = db.Column(db.String(128))
    chk_time = db.Column(db.DateTime)
    domain = db.Column(db.Text)
    elb = db.Column(db.Text)
    ip = db.Column(db.Text)

    def __init__(self, _dict):
        for k, v in _dict.items():
            if "time" in k:
                setattr(self, k, datetime.strptime(v, "%Y-%m-%d"))
            else:
                setattr(self, k, v)

    @staticmethod
    def add(_dict):
        icp = Icp(_dict)
        db.session.add(icp)
        db.session.commit()
        return icp

    @staticmethod
    def delete(did):
        icp = Icp.query.filter(Icp.id == did).one()
        db.session.delete(icp)
        db.session.commit()
        return True

    @staticmethod
    def _to_dict(icp):
        _dict = icp.to_dict()
        _dict["domain"] = icp.domain
        return _dict

    @staticmethod
    def select():
        return [Icp._to_dict(i) for i in Icp.query.all()]

    @staticmethod
    @db.transaction
    def edit(_dict):
        Database.to_cls(Icp, _dict)
        db.session.flush()
        return True

    @staticmethod
    def get(iid):
        return Icp._to_dict(Icp.query.filter(Icp.id == iid).one())


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
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
        _dict["connector"] = session[USER_SESSION]["uid"]
        if not _dict.__contains__("path"): _dict["path"] = ""
        new_supplier = Supplier(_dict)
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
        supplier.path = _dict["path"]
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
        return Supplier.query.filter(Supplier.id == sid).one().to_dict()


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(128))
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))
    path = db.Column(db.String(256))  # 合同文件路径

    def __init__(self, _dict):
        if _dict.__contains__("id"):
            return

        if _dict["begin_time"]:
            self.begin_time = datetime.strptime(_dict["begin_time"], "%Y-%m-%d")
        else:
            self.begin_time = datetime.now()
        if _dict["end_time"]:
            self.end_time = datetime.strptime(_dict["end_time"], "%Y-%m-%d")
        else:
            self.end_time = datetime.now()

        if _dict.__contains__("path"):
            self.path = _dict["path"]
        else:
            self.path = ""

        if _dict.__contains__("desc"):
            self.desc = _dict["desc"]

    @staticmethod
    def add(_dict):
        contract = Contract(_dict)
        db.session.add(contract)
        db.session.commit()
        return contract

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
        contract.path = _dict["path"]

        if _dict.__contains__("purchase_id") and _dict["purchase_id"]:
            contract.purchase_id = _dict["purchase_id"]

        if _dict.__contains__("desc"):
            contract.desc = _dict["desc"]

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

    @staticmethod
    def get(id):
        return Contract._to_dict(Contract.query.filter(Contract.id == id).one())


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    parent_id = db.Column(db.Integer)
    is_del = db.Column(db.Boolean, default=False)

    def __init__(self, _dict):
        self.name = _dict["name"]
        self.parent_id = _dict["parent_id"]

    @staticmethod
    @db.transaction
    def add(_dict):
        query = Category.query \
            .filter(Category.parent_id == _dict["parent_id"]) \
            .filter(Category.name == _dict["name"])

        def is_exist(is_del):
            if query.filter(Category.is_del == is_del).count():
                return True
            return False

        if is_exist(is_del=False):
            raise ExceptionEx("分类%s已经存在" % _dict["name"])

        if is_exist(is_del=True):
            category = query.one()
            category.is_del = False
        else:
            db.session.add(Category(_dict))

        db.session.flush()
        return True

    @staticmethod
    @db.transaction
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

        for child in category.all():
            Category.__delete(child.to_dict())

        category = Category.query.filter(Category.id == id).one()
        category.is_del = True

    @staticmethod
    @db.transaction
    def delete(id):
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
    def select(parent_id):
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


class StockOpt(db.Model):
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

        Stock.init(self, _dict)

    @staticmethod
    def add(_dict):
        db.session.add(StockOpt(_dict))
        db.session.commit()
        return True

    @staticmethod
    @db.transaction
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
        stock = Stock._to_dict(self.stock, False)
        opt = self.to_dict()
        opt["stock"] = stock
        return opt

    @staticmethod
    def select(type, page, pre_page):
        page = StockOpt.query \
            .filter(StockOpt.type == type) \
            .order_by(StockOpt.time.desc()) \
            .order_by(StockOpt.update_time.desc()) \
            .paginate(page, pre_page)
        return page.to_page(StockOpt._to_dict)

    @staticmethod
    def approvals(page, pre_page):  # todo 添加报废的审批组
        page = StockOpt.query \
            .filter(StockOpt.type == SCRAP.TYPE) \
            .filter(StockOpt.status.in_(["", SCRAP.PASS, SCRAP.FAIL])).paginate(page, pre_page)
        return page.to_page(StockOpt._to_dict)

    @staticmethod
    def get(type, id):
        return StockOpt._to_dict(StockOpt.query \
                                 .filter(StockOpt.type == type) \
                                 .filter(StockOpt.id == id).one())

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


class Stock(db.Model):
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

    @staticmethod
    def init(self, _dict):
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

    def __init__(self, _dict):
        Stock.init(self, _dict)

    @staticmethod
    @db.transaction
    def add(_dict):
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
        db.session.flush()
        return stock

    @staticmethod
    @db.transaction
    def edit(_dict):
        if Stock.query.filter(Stock.no == _dict["no"]).count():
            raise ExceptionEx("库存编号已存在")

        stock = Database.to_cls(Stock, _dict)
        db.session.flush()

    @staticmethod
    @db.transaction
    def delete(id):
        stock = Stock.query.filter(Stock.id == id).one()
        for opt in stock.opts:
            db.session.delete(opt)
        db.session.delete(stock)
        db.session.flush()

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

    @staticmethod
    def get(id):
        return Stock._to_dict(Stock.query.filter(Stock.id == id).one(), True)

    @staticmethod
    def select(page, pre_page, nan_opt):
        query = Stock.query.order_by(Stock.stock_in_time.desc())
        if nan_opt:
            opts = StockOpt.query.filter(StockOpt.status.in_(["", SCRAP.PASS, SCRAP.TYPE])).all()
            in_opts = [opt.stock_id for opt in opts]
            query = query.filter(~Stock.id.in_(in_opts))
        page = query.paginate(page, pre_page)
        return page.to_page(Stock._to_dict)


if __name__ == "__main__":
    pass
