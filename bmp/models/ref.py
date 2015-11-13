# coding: utf-8
from bmp import db


class Ref(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), nullable=False)

    def __init__(self, name, type):
        self.name = name
        self.type = type

    @staticmethod
    def select(type):
        refs = Ref.query.filter(Ref.type.like(type)).all()
        return [ref.to_dict() for ref in refs]


    @staticmethod
    @db.transaction
    def add(name, type):
        if Ref.query \
                .filter(Ref.type == type) \
                .filter(Ref.name == name).count():
            return False

        db.session.add(Ref(name, type))
        db.session.flush()



    @staticmethod
    def get(id):
        return Ref.query.filter(Ref.id==id).one().to_dict()
