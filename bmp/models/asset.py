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


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    begin_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))
    supplier_name = db.Column(db.String(128), db.ForeignKey("supplier.name"))
    path = db.Column(db.String(256))  # 合同文件路径

    def __init__(self,_dict):
        self.begin_time=datetime.strptime(_dict["begin_time"],"%Y-%m-%d %H:%M")
        self.end_time=datetime.strptime(_dict["end_time"],"%Y-%m-%d %H:%M")
        self.purchase_id = _dict["purchase_id"]
        self.supplier_name = _dict["supplier_name"]
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


    def __init__(self, _dict):
        self.name = _dict["name"]
        self.parent_id = _dict["parent_id"]

    @staticmethod
    def add(_dict):
        print type(db.session)
        print _dict
        db.session.add(Category(_dict))
        db.session.commit()
        return True

    @staticmethod
    def edit(id,_dict):
        print 'yy:', id,  _dict
        category = Category.query.filter(Category.id==id).one()
        category.name = _dict["name"]
        category.parent_id = _dict["parent_id"]
        db.session.commit()
        return True


    # 递归算法
    @staticmethod
    def __delete(id):
        # 若category.count() == 0  说明当前删除的记录是叶子节点；反之，删除的是非叶子节点
        category = Category.query.filter(Category.parent_id == id)
        # 非叶子节点的删除
        if category.count():
            for child in category.all():
                Category.__delete(child.to_dict())

        # 删除叶子节点
        db.session.delete(Category.query.filter(Category.id == id).one())

    @staticmethod
    @db.transaction
    def delete(id):
        Category.__delete(id)

    # 也要写递归?  给一个id,同一级别的所有id均要出来
    # 特点：一、没有parent_id的，均是一级根节点    二、

    @staticmethod
    def middle_history(category, one_result_par_id):
        all_child = []
        for cur_each in category.all():
            cur_each = cur_each.to_dict()
            child = Category.query.filter(Category.parent_id == cur_each["id"])
            # print 'aaa', child
            for each_child in child:
                each_child = each_child.to_dict()
                if each_child["parent_id"] == one_result_par_id:
                    return [result.to_dict() for result in child.all()]
                else:
                    continue
            all_child.append(child)   # ????
        Category.middle_history(all_child)



    # 非根节点情况
    @staticmethod
    def __history(_dict, one_result_par_id):
        # 非顶层  则一直往上层退
        if _dict["parent_id"]:
            up_example = Category.query.filter(Category.id == _dict["parent_id"]).first()
            Category.__history(up_example)
        # 退到了最顶层
        else:
            root = Category.query.filter(Category.parent_id == None)
            Category.middle_history(root, one_result_par_id)

    @staticmethod
    @db.transaction
    def history(parent_id, _dict):
        if not _dict["parent_id"]:
            root_category = Category.query.filter(Category.parent_id == None)
            return [each_root.to_dict() for each_root in root_category.all()]
        else:
            Category.__history(_dict, parent_id)




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
