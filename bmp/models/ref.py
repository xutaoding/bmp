#coding: utf-8
from bmp import db

class Ref(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(128),nullable=False)
    type=db.Column(db.String(128),nullable=False)

    def __init__(self,name,type):
        self.name=name
        self.type=type

    @staticmethod
    def select(type):
        refs=Ref.query.filter(Ref.type.like(type)).all()
        return [ref.to_dict() for ref in refs]