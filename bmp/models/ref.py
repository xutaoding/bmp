# coding: utf-8
from bmp import db
from bmp.utils.exception import ExceptionEx


class Ref(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    parent_id = db.Column(db.Integer, default=0)

    def __init__(self, name, type, parent_id):
        self.name = name
        self.type = type
        self.parent_id = parent_id

    @staticmethod
    def select(type):
        refs = Ref.query.filter(Ref.type.like(type)).all()
        return [ref.to_dict() for ref in refs]

    @staticmethod
    def map(type):
        refs={}
        for ref in Ref.select(type):
            refs[ref["id"]]=ref["name"]
        return refs


    @staticmethod
    def add(name, type, parent_id=0):
        if Ref.query \
                .filter(Ref.type == type) \
                .filter(Ref.name == name) \
                .filter(Ref.parent_id == parent_id).count():
            raise ExceptionEx("该分类已存在")

        db.session.add(Ref(name, type, parent_id))
        db.session.commit()

    @staticmethod
    def delete(id):
        db.session.delete(Ref.query.filter(Ref.id == id).one())

    @staticmethod
    def get(id):
        return Ref.query.filter(Ref.id == id).one().to_dict()
