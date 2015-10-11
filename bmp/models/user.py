#coding: utf-8
from bmp import db

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    uid=db.Column(db.String(128),unique=True)
    displayName=db.Column(db.String(128))
    mail=db.Column(db.String(128))
    mobile=db.Column(db.String(128))
    title=db.Column(db.String(128))

    def __init__(self,_dict):
        self.id=0
        for k,lst_item in _dict.items():
            setattr(self,k,lst_item[0])


if __name__=="__main__":
    pass