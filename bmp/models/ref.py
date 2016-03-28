# coding: utf-8
from bmp import db
from bmp.utils.exception import ExceptionEx


class Ref(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    parent_id = db.Column(db.Integer, default=0)
    is_del = db.Column(db.Boolean, default=False)

    def __init__(self, name, type, parent_id):
        self.name = name
        self.type = type
        self.parent_id = parent_id

    @staticmethod
    def select(type):
        refs = Ref.query.filter(Ref.type.like(type)).filter(Ref.is_del!=True).all()
        return [ref.to_dict() for ref in refs]

    @staticmethod
    def map(type):
        refs = {}
        for ref in Ref.select(type):
            refs[ref["id"]] = ref["name"]
        return refs

    @staticmethod
    def add(name, type, parent_id=0):
        query = Ref.query \
            .filter(Ref.type == type) \
            .filter(Ref.name == name) \
            .filter(Ref.parent_id == parent_id)

        if query.filter(Ref.is_del != True).count():
            raise ExceptionEx("该分类已存在")

        if query.filter(Ref.is_del).count():
            ref = query.filter(Ref.is_del).one()
            ref.is_del = False
        else:
            db.session.add(Ref(name, type, parent_id))
        db.session.commit()

    @staticmethod
    def delete(rid):
        ref = Ref.query.filter(Ref.id == rid).one()
        ref.is_del = True
        db.session.commit()

    @staticmethod
    def get(id):
        return Ref.query.filter(Ref.id == id).one().to_dict()


    @staticmethod
    def _to_dict(self):
        return self.to_dict()