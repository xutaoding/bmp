#coding: utf-8
from bmp import db

class Ref(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(128))
    type=db.Column(db.String(128))

    def __init__(self,name,type):
        self.name=name
        self.type=type
