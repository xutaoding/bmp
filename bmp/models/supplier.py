# coding: utf-8

from bmp import db
from datetime import datetime

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    connector = db.Column(db.String(128))
    mobile = db.Column(db.String(128))
    address = db.Column(db.String(128))
    interfaceor = db.Column(db.String(128))
    create_time = db.Column(db.DateTime)
    last_time = db.Column(db.DateTime)

    def __init__(self, _dict):
        for key, value in _dict.items():
            setattr(self, key, value)

    @staticmethod
    def add(_dict):
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
    def edit(id, _dict):
        supplier = Supplier.query.filter(Supplier.id == id).one()
        db.session.delete(supplier)
        Supplier.add(_dict)
        db.session.commit()
        return True


    @staticmethod
    def get(rid):
        return Supplier.query.filter(Supplier.id == rid).one()


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    signDate = db.Column(db.String(128))
    stopDate = db.Column(db.String(128))
    buyer = db.Column(db.String(128))
    seller = db.Column(db.String(128))
    content = db.Column(db.String(800))
    detailed = db.Column(db.String(1600))
    create_time = db.Column(db.DateTime)
    last_time = db.Column(db.DateTime)

    def __init__(self, _dict):
        for key, value in _dict.items():
            setattr(self, key, value)

    @staticmethod
    def add(_dict):
        new_contract = Contract(_dict)
        new_contract.create_time = datetime.now()
        new_contract.last_time = datetime.now()
        db.session.add(new_contract)
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
        db.session.delete(contract)
        Contract.add(_dict)
        db.session.commit()
        return True

    @staticmethod
    def get(rid):
        return Contract.query.filter(Contract.id == rid).one()


